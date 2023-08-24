# SSDR Implementation in Python
# Dalton Omens

import maya.api.OpenMaya as om
import numpy as np
from scipy.optimize import lsq_linear
from scipy.cluster.vq import vq, kmeans, whiten
import time


def kabsch(P, Q):
    """
    kabsch算法（点云配准算法）：有两个点集P和Q，这两个点集的点一一对应，但是P和Q并不重合
    假设P受到一根骨骼的影响，那么如何旋转和平移这根骨骼，使得最终变换后的P'与Q的差异最小？
    Computes the optimal translation and rotation matrices that minimize the
    RMS deviation between two sets of points P and Q using Kabsch's algorithm.
    More here: https://en.wikipedia.org/wiki/Kabsch_algorithm
    Inspiration: https://github.com/charnley/rmsd

    inputs: P  N x 3 numpy matrix representing the coordinates of the points in P
            Q  N x 3 numpy matrix representing the coordinates of the points in Q

    return: A 4 x 3 matrix where the first 3 rows are the rotation and the last is translation
    """
    if P.size == 0 or Q.size == 0:
        raise ValueError("Empty matrices sent to kabsch")
    centroid_P = np.mean(P, axis=0)
    centroid_Q = np.mean(Q, axis=0)
    # 均值归一到0
    P_centered = P - centroid_P  # Center both matrices on centroid
    Q_centered = Q - centroid_Q
    H = P_centered.T.dot(Q_centered)  # covariance matrix
    U, S, V = np.linalg.svd(H)  # SVD
    R = U.dot(V).T  # calculate optimal rotation
    # 这里变换为右手系
    if np.linalg.det(R) < 0:  # correct rotation matrix for
        V[2, :] *= -1  # right-hand coordinate system
        R = U.dot(V).T
    t = centroid_Q - R.dot(centroid_P)  # translation vector
    # 反正最终返回的就是一个transform，注意这是一个右乘矩阵，即使一个4行3列的矩阵
    return np.vstack((R, t))


def initialize(poses, rest_pose, num_bones, iterations=5):
    """
    Uses the k-means algorithm to initialize bone transformations.

    inputs: poses       |num_poses| x |num_verts| x 3 matrix representing coordinates of vertices of each pose
            rest_pose   |num_verts| x 3 numpy matrix representing the coordinates of vertices in rest pose
            num_bones   Number of bones to initialize
            iterations  Number of iterations to run the k-means algorithm

    return: A |num_bones| x |num_poses| x 4 x 3 matrix representing the stacked Rotation and Translation
              for each pose, for each bone.
            A |num_bones| x 3 matrix representing the translations of the rest bones.
    """
    # rest_pose：建模姿态
    num_verts = rest_pose.shape[0]
    num_poses = poses.shape[0]
    # 每个骨骼每一帧的trans
    # bone_transforms: (num_bones, num_poses, 4, 3)
    bone_transforms = np.empty(
        (num_bones, num_poses, 4, 3)
    )  # [(R, T) for for each pose] for each bone
    # 3rd dim has 3 rows for R and 1 row for T
    rest_bones_t = np.empty((num_bones, 3))  # Translations for bones at rest pose
    rest_pose_corrected = np.empty(
        (num_bones, num_verts, 3)
    )  # Rest pose - mean of vertices attached to each bone

    # Use k-means to assign bones to vertices
    # 白化：rest_pose / 每一列的标准差，即x，y，z三个轴的标准差，这个只是为了kmeans用的
    whitened = whiten(rest_pose)
    # 直接将白化后的rest pose进行kmeans分组，分组的数量就是骨骼的数量
    # python用了两个函数来完成这一步
    # kmeans返回的是中心点
    codebook, _ = kmeans(whitened, num_bones)
    # 将白化的初始顶点与中心点绑定，就完成了分组
    # vert_assignments: (num_verts,)
    vert_assignments, _ = vq(
        whitened, codebook
    )  # Bone assignment for each vertex (|num_verts| x 1)

    # 遍历所有骨骼
    # Compute initial random bone transformations
    for bone in range(num_bones):
        #  计算中心点，每个vert都有一个骨骼的assignment，每个骨骼的所有顶点作为一个cluster，来计算中心
        # rest pose下，当前bone对应cluster的中心
        # rest_bones_t:(num_bones, 3)
        rest_bones_t[bone] = np.mean(rest_pose[vert_assignments == bone], axis=0)
        # 这个corrected就是各个顶点相对于所属cluster的中心点的偏移
        # rest_pose: (num_verts, 3)
        # rest_pose_corrected: (num_bones, num_verts, 3)
        # 将rest pose中的各个顶点减去中心点，这里需要注意的就是，这里是计算的所有的顶点
        # 也就是说，这里是把全身所有的顶点相对于一根骨骼的cluster的中心的位置
        rest_pose_corrected[bone] = rest_pose - rest_bones_t[bone]
        # rest_pose_corrected[bone] = rest_pose - np.mean(rest_pose[vert_assignments == bone], axis=0)

        # 现在我们有了rest pose接着遍历每个pose
        for pose in range(num_poses):
            # 传入的相对于中心点的rest pose的坐标，以及当前这一帧pose的顶点数据
            # 对于一根骨骼，可能会有多个顶点绑定到这根骨骼上，因此对于一根骨骼而言，它对应了一个点集
            # 因此kabsch算法的目标，就是尝试去旋转和平移这根骨骼，使得这两个点集的差异最小
            # 计算该骨骼在当前这一帧下的transform
            # rest_pose_corrected里面是所有的顶点，但这里只取了属于这个骨骼的顶点，用kabsch算法来计算当前这根骨骼的transform
            bone_transforms[bone, pose] = kabsch(
                rest_pose_corrected[bone, vert_assignments == bone],
                poses[pose, vert_assignments == bone],
            )

    for it in range(iterations):
        # Re-assign bones to vertices using smallest reconstruction error from all poses
        # 这里重新构造了每个骨骼，每一帧，所有顶点的空间
        # constructed: (num_bones, num_poses, num_verts, 3)
        constructed = np.empty(
            (num_bones, num_poses, num_verts, 3)
        )  # |num_bones| x |num_poses| x |num_verts| x 3
        for bone in range(num_bones):
            # 遍历每根骨骼
            # 变换顶点到模型空间
            # 先旋转
            # 由于该矩阵是4行3列，这里取了矩阵前三行，即旋转矩阵。
            # 将rest pose的顶点位置设置到所属骨骼空间下，之后进行旋转
            # 顶点进行旋转之后，将顶点的yz两个轴对调了，变为右手系，上面构造bone_transforms的kabsch函数中也有变换手系的操作
            # 不过这里相当于rest pose下所有顶点在所有帧都进行了一次变换
            # bone_transforms: (num_bones, num_poses, 4, 3)
            Rp = (
                bone_transforms[bone, :, :3, :]
                .dot((rest_pose - rest_bones_t[bone]).T)
                .transpose((0, 2, 1))
            )  # |num_poses| x |num_verts| x 3
            # 再平移
            # R * p + T
            constructed[bone] = Rp + bone_transforms[bone, :, np.newaxis, 3, :]
        # 变换后的顶点位置与原始pose做比较
        # 计算2范数，即平方和再开方
        # 后面的axis=(1,3)，1对应的是 poses, 3对应的是位置，也就是说，是针对这所有帧的顶点位置差异计算2范数
        # 即遍历num_bones和num_verts，所有元素平方求和再开根号
        # constructed: (num_bones, num_poses, num_verts, 3)
        # errs: (num_bones, num_verts)
        errs = np.linalg.norm(constructed - poses, axis=(1, 3))
        # 上面我们计算了errors，其结构是(num_bones, num_verts)，是每根骨骼，每个顶点（与是否隶属于该骨骼无关），在整个动画序列中的error
        # 对于每一根骨骼，按列，即寻找最小的顶点索引，即每个顶点的位置上保存了error最小的骨骼的索引。于是我们有了一个新的映射
        # (num_verts)，
        vert_assignments = np.argmin(errs, axis=0)

        # Visualization of vertex assignments for bone 0 over iterations
        # Make 5 copies of an example pose mesh and call them test0, test1...
        # for i in range(num_verts):
        #    if vert_assignments[i] == 0:
        #        pm.select('test{0}.vtx[{1}]'.format(it, i), add=True)
        # print(vert_assignments)

        # For each bone, for each pose, compute new transform using kabsch
        for bone in range(num_bones):
            # 根据新的骨骼映射，重新计算cluster中心点
            rest_bones_t[bone] = np.mean(rest_pose[vert_assignments == bone], axis=0)
            # 计算所有顶点相对于每根骨骼的位置
            rest_pose_corrected[bone] = rest_pose - np.mean(
                rest_pose[vert_assignments == bone], axis=0
            )
            # 重新使用kabsch算法，来计算骨骼变换
            for pose in range(num_poses):
                # 这里依然是根据vert_assignments，以某根骨骼下的所有顶点为依据，计算该骨骼的transform
                bone_transforms[bone, pose] = kabsch(
                    rest_pose_corrected[bone, vert_assignments == bone],
                    poses[pose, vert_assignments == bone],
                )
    # 最后返回的是骨骼的动画数据，以及骨骼在rest pose下的位置
    return bone_transforms, rest_bones_t


def update_weight_map(bone_transforms, rest_bones_t, poses, rest_pose, sparseness):
    """
    Update the bone-vertex weight map W by fixing bone transformations and using a least squares
    solver subject to non-negativity constraint, affinity constraint, and sparseness constraint.

    inputs: bone_transforms |num_bones| x |num_poses| x 4 x 3 matrix representing the stacked
                                Rotation and Translation for each pose, for each bone.
            rest_bones_t    |num_bones| x 3 matrix representing the translations of the rest bones
            poses           |num_poses| x |num_verts| x 3 matrix representing coordinates of vertices of each pose
            rest_pose       |num_verts| x 3 numpy matrix representing the coordinates of vertices in rest pose
            sparseness      Maximum number of bones allowed to influence a particular vertex

    return: A |num_verts| x |num_bones| weight map representing the influence of the jth bone on the ith vertex
    """
    num_verts = rest_pose.shape[0]
    num_poses = poses.shape[0]
    num_bones = bone_transforms.shape[0]

    W = np.empty((num_verts, num_bones))

    for v in range(num_verts):
        # 遍历所有顶点
        # For every vertex, solve a least squares problem
        Rp = np.empty((num_bones, num_poses, 3))
        # 变换当前这个顶点，用所有骨骼去变换，得到变换后的顶点
        for bone in range(num_bones):
            Rp[bone] = bone_transforms[bone, :, :3, :].dot(
                rest_pose[v] - rest_bones_t[bone]
            )  # |num_bones| x |num_poses| x 3
        # R * p + T
        Rp_T = Rp + bone_transforms[:, :, 3, :]  # |num_bones| x |num_poses| x 3
        # 这个就是变换后的顶点位置，这里相当于把所有pose的每个xyz都按行展开了
        # （num_bones, nun_poses, 3）->(num_poses, 3, num_bones) -> (3 * num_poses, num_bones)
        A = Rp_T.transpose((1, 2, 0)).reshape(
            (3 * num_poses, num_bones)
        )  # 3 * |num_poses| x |num_bones|
        # 这个是真正的顶点位置
        b = poses[:, v, :].reshape(3 * num_poses)  # 3 * |num_poses| x 1
        # 计算x在什么时候，Ax - b的差异最小，用的是mse。这里用带bound的线性回归去做，因为所有权重的值只能在[0],1]之间
        # 最终得到了每根骨骼的权重
        # Bounds ensure non-negativity constraint and kind of affinity constraint
        w = lsq_linear(A, b, bounds=(0, 1), method="bvls").x  # |num_bones| x 1
        # 骨骼权重归一化
        w /= np.sum(w)  # Ensure that w sums to 1 (affinity constraint)

        # 由于每一个顶点有一个最大权重的数量限制|K|，因此我们要抛弃其他的
        # Remove |B| - |K| bone weights with the least "effect"
        # 在这里重新reshape一下A*w，得到了拟合后的顶点
        # (3 * num_poses, num_bones) -> (num_poses, 3, num_bones)
        # 然后根据列1，求二范数，即遍历num_poses和num_bones，所有元素平方求和开根号，其实就是顶点位置的2范数
        effect = np.linalg.norm(
            (A * w).reshape(num_poses, 3, num_bones), axis=1
        )  # |num_poses| x |num_bones|
        # 然后又把num_poses给合并了，这里其实干的事情，就是去求当前顶点受到不同骨骼影响的程度，我们就可以知道应该干掉哪些骨骼了
        effect = np.sum(effect, axis=0)  # |num_bones| x 1
        # 因为一个顶点最多只能被|k|根骨骼所影响，因此这里计算要被抛弃的骨骼数量
        num_discarded = max(num_bones - sparseness, 0)
        # np.argpartition是将数组内容分组，比num_discarded小的放前面，比它大的放后面，
        # 因此这里实际上就是抛弃掉最小的num_discarded个元素
        # 这里的effective保存了每个顶点所选取的骨骼的索引：数量为：|sparseness|
        effective = np.argpartition(effect, num_discarded)[
            num_discarded:
        ]  # |sparseness| x 1

        # 到现在位置，我们知道了每个顶点到底要绑定哪些骨骼
        # 只使用我们选取的那几根骨骼，重新线性回归来算权重
        # Run least squares again, but only use the most effective bones
        A_reduced = A[:, effective]  # 3 * |num_poses| x |sparseness|
        w_reduced = lsq_linear(
            A_reduced, b, bounds=(0, 1), method="bvls"
        ).x  # |sparseness| x 1
        w_reduced /= np.sum(w_reduced)  # Ensure that w sums to 1 (affinity constraint)

        # 最终，得到了当前顶点的权重稀疏矩阵
        w_sparse = np.zeros(num_bones)
        # 我们选取的那几根骨骼，设置为重新算好的权重
        w_sparse[effective] = w_reduced
        w_sparse /= np.sum(
            w_sparse
        )  # Ensure that w_sparse sums to 1 (affinity constraint)

        W[v] = w_sparse
    # 返回所有顶点的权重赋值关系
    # (num_verts, num_bones)
    return W


def update_bone_transforms(W, bone_transforms, rest_bones_t, poses, rest_pose):
    """
    Updates the bone transformations by fixing the bone-vertex weight map and minimizing an
    objective function individually for each pose and each bone.

    inputs: W               |num_verts| x |num_bones| matrix: bone-vertex weight map. Rows sum to 1, sparse.
            bone_transforms |num_bones| x |num_poses| x 4 x 3 matrix representing the stacked
                                Rotation and Translation for each pose, for each bone.
            rest_bones_t    |num_bones| x 3 matrix representing the translations of the rest bones
            poses           |num_poses| x |num_verts| x 3 matrix representing coordinates of vertices of each pose
            rest_pose       |num_verts| x 3 numpy matrix representing the coordinates of vertices in rest pose

    return: |num_bones| x |num_poses| x 4 x 3 matrix representing the stacked
                                Rotation and Translation for each pose, for each bone.
    """
    num_bones = W.shape[1]
    num_poses = poses.shape[0]
    num_verts = W.shape[0]
    # 遍历所有pose
    for pose in range(num_poses):
        # 遍历当前pose下的所有骨骼
        for bone in range(num_bones):
            # 计算rest pose下所有顶点相对于当前骨骼的偏移
            # Represents the points in rest pose without this rest bone's translation
            p_corrected = rest_pose - rest_bones_t[bone]  # |num_verts| x 3

            # Calculate q_i for all vertices by equation (6)
            # (num_bones, num_verts, 3)
            constructed = np.empty(
                (num_bones, num_verts, 3)
            )  # |num_bones| x |num_verts| x 3

            for bone2 in range(num_bones):
                # 遍历所有骨骼
                #  首先计算rest pose以bone2的
                # 提取出当前骨骼的旋转矩阵，将rest pose相对于当前骨骼来算出local position，将其旋转
                # can't use p_corrected before because we want to correct for every bone2 distinctly
                # (num_verts, 3)
                Rp = (
                    bone_transforms[bone2, pose, :3, :]
                    .dot((rest_pose - rest_bones_t[bone2]).T)
                    .T
                )  # |num_verts| x 3
                #  然后平移，这里就得到了每一帧动画，被每一根骨骼变换后的顶点位置
                # 由于有权重来表明了哪个顶点会被哪些骨骼所影响，所以对于任何一根骨骼，这里算全部顶点的
                # R * p + T
                constructed[bone2] = Rp + bone_transforms[bone2, pose, 3, :]
            # w * (R * p + T)
            # 这里把顶点乘以对应的权重，注意经过上一步，这里的权重大多数都是0了，只有重要的权重才有数值，数量最多为|K|
            # 因此这里得到的是每个顶点相对于其对应骨骼的加权位置，后面要求和，得到真正位置
            # (num_bones, num_verts, 3)->(num_verts, num_bones, 3)
            constructed = (
                constructed.transpose((1, 0, 2)) * W[:, :, np.newaxis]
            )  # |num_verts| x |num_bones| x 3
            # 这里的操作，就是要将这些位置，干掉当前骨骼这一列，用于去掉当前骨骼的影响
            constructed = np.delete(
                constructed, bone, axis=1
            )  # |num_verts| x |num_bones-1| x 3
            # 当前骨骼是我们关注的骨骼，因此q就是真正的顶点位置减去其他骨骼对该顶点的影响，得到的点云
            # 直观的理解，就是pose是真实的点云，而去掉当前骨骼的constructed points是一个估计后的点云，
            q = poses[pose] - np.sum(constructed, axis=1)  # |num_verts| x 3

            # 而p是rest pose下的顶点相对于中心点的偏移的点云，这个中心点是一个加权平均，权重与该顶点的对于骨骼的w有关
            # p_star是rest pose下的中心点
            # q_star是当前动画的残差的中心点
            # Calculate p_star, q_star, p_bar, and q_bar for all verts by equation (8)
            p_star = np.sum(
                np.square(W[:, bone, np.newaxis]) * p_corrected, axis=0
            )  # |num_verts| x 3 => 3 x 1
            p_star /= np.sum(np.square(W[:, bone]))  # 3 x 1

            q_star = np.sum(
                W[:, bone, np.newaxis] * q, axis=0
            )  # |num_verts| x 3 => 3 x 1
            q_star /= np.sum(np.square(W[:, bone]))  # 3 x 1
            # 至此得到了两个点云，
            p_bar = p_corrected - p_star  # |num_verts| x 3
            q_bar = q - W[:, bone, np.newaxis] * q_star  # |num_verts| x 3
            # 下面进行点云配准，得到骨骼的旋转和平移
            # Perform SVD by equation (9)
            P = (p_bar * W[:, bone, np.newaxis]).T  # 3 x |num_verts|
            Q = q_bar.T  # 3 x |num_verts|
            # 点云配准得到旋转矩阵
            U, S, V = np.linalg.svd(np.matmul(P, Q.T))

            # Calculate rotation R and translation t by equation (10)
            R = U.dot(V).T  # 3 x 3
            t = q_star - R.dot(p_star)  # 3 x 1

            bone_transforms[bone, pose, :3, :] = R
            bone_transforms[bone, pose, 3, :] = t
    # 最终返回，每根骨骼在每一帧的pose
    return bone_transforms


def SSDR(poses, rest_pose, num_bones, sparseness=4, max_iterations=20):
    """
    Computes the Smooth Skinning Decomposition with Rigid bones

    inputs: poses           |num_poses| x |num_verts| x 3 matrix representing coordinates of vertices of each pose
            rest_pose       |num_verts| x 3 numpy matrix representing the coordinates of vertices in rest pose
            num_bones       number of bones to create
            sparseness      max number of bones influencing a single vertex

    return: An i x j matrix of bone-vertex weights, where i = # vertices and j = # bones
            A length-B list of (length-t lists of bone transformations [R_j | T_j] ), one list for each bone
            A list of bone translations for the bones at rest
    """
    start_time = time.time()
    # 初始化，给定动画帧poses，和t pose，以及需要多少根骨骼，返回所有骨骼的变换矩阵，以及各个骨骼的中心点
    bone_transforms, rest_bones_t = initialize(poses, rest_pose, num_bones)
    for _ in range(max_iterations):
        W = update_weight_map(
            bone_transforms, rest_bones_t, poses, rest_pose, sparseness
        )
        bone_transforms = update_bone_transforms(
            W, bone_transforms, rest_bones_t, poses, rest_pose
        )
        print(
            "Reconstruction error:",
            reconstruction_err(poses, rest_pose, bone_transforms, rest_bones_t, W),
        )

    end_time = time.time()
    print("Done. Calculation took {0} seconds".format(end_time - start_time))
    print(
        "Avg reconstruction error:",
        reconstruction_err(poses, rest_pose, bone_transforms, rest_bones_t, W),
    )

    return W, bone_transforms, rest_bones_t


def reconstruction_err(poses, rest_pose, bone_transforms, rest_bones_t, W):
    """
    Computes the average reconstruction error on some poses given bone transforms and weights.

    inputs : poses           |num_poses| x |num_verts| x 3 matrix representing coordinates of vertices of each pose
             rest_pose       |num_verts| x 3 numpy matrix representing the coordinates of vertices in rest pose
             bone_transforms |num_bones| x |num_poses| x 4 x 3 matrix representing the stacked
                                Rotation and Translation for each pose, for each bone.
             rest_bones_t    |num_bones| x 3 matrix representing the translations of the rest bones
             W               |num_verts| x |num_bones| matrix: bone-vertex weight map. Rows sum to 1, sparse.

    return: The average reconstruction error v - sum{bones} (w * (R @ p + T))
    """
    num_bones = bone_transforms.shape[0]
    num_verts = W.shape[0]
    num_poses = poses.shape[0]
    # 计算rest pose本地相对于各个骨骼的偏移
    # Points in rest pose without rest bone translations
    # rest_pose: (num_verts, 3)->(1, num_verts, 3)
    # rest_bones_t:(num_bones, 3)->(num_bones, 1, 3)
    # pcorrected:( num_bones, num_verts, 3)
    p_corrected = (
        rest_pose[np.newaxis, :, :] - rest_bones_t[:, np.newaxis, :]
    )  # |num_bones| x |num_verts| x 3
    constructions = np.empty(
        (num_bones, num_poses, num_verts, 3)
    )  # |num_bones| x |num_poses| x |num_verts| x 3
    # 进行旋转变换
    for bone in range(num_bones):
        # When you are a vectorizing GOD
        constructions[bone] = np.einsum(
            "ijk,lk->ilj", bone_transforms[bone, :, :3, :], p_corrected[bone]
        )  # |num_poses| x |num_verts| x 3
    # 加上偏移
    constructions += bone_transforms[
        :, :, np.newaxis, 3, :
    ]  # |num_bones| x |num_poses| x |num_verts| x 3
    # 算上权重，得到最终拟合顶点
    constructions *= (W.T)[
        :, np.newaxis, :, np.newaxis
    ]  # |num_bones| x |num_poses| x |num_verts| x 3
    # 真正pose减去拟合的pose，得到残差errors
    errors = poses - np.sum(constructions, axis=0)  # |num_poses| x |num_verts| x 3
    # 算二范数作为最终error
    return np.mean(np.linalg.norm(errors, axis=2))


# Get numpy vertex arrays from selected objects. Rest pose is most recently selected.

selectionLs = om.MGlobal.getActiveSelectionList()
num_poses = selectionLs.length() - 1
rest_pose = np.array(
    om.MFnMesh(selectionLs.getDagPath(num_poses)).getPoints(om.MSpace.kWorld)
)[:, :3]
poses = np.array(
    [
        om.MFnMesh(selectionLs.getDagPath(i)).getPoints(om.MSpace.kWorld)
        for i in range(num_poses)
    ]
)[:, :, :3]

W, bone_transforms, rest_bones_t = SSDR(poses, rest_pose, 2)
