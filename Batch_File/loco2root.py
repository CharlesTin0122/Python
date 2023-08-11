# -*- coding: utf-8 -*-
"""
@FileName      : loco2root.py
@DateTime      : 2023/08/03 15:57:37
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
"""
import pymel.core as pm
import pymel.core.nodetypes as nt
import pymel.core.datatypes as dt


def loco_anim2root_anim(
    pelvis_jnt: nt.Joint, root_jnt: nt.Joint, root_pelvis_matrix: dt.Matrix
) -> None:
    """原地动画转根骨骼动画

    Args:
        pelvis_jnt (nt.Joint): 胯骨骼
        root_jnt (nt.Joint): 根骨骼
        root_pelvis_matrix (dt.Matrix): 根骨骼到胯骨骼之间的变换矩阵，具体算法如下，
        方法1.在胯骨骼和根骨骼位置各创建一个locator,将根骨骼locator设为胯骨骼locator的子物体，用根骨骼locator.getMatrix()得到他们之间的变换矩阵。
        方法2.获得胯骨骼和根骨骼的世界矩阵，然后根骨骼世界矩阵左乘胯骨骼世界逆矩阵得到根骨骼到胯骨骼的变换矩阵。
    """

    start_frame = pm.findKeyframe(pelvis_jnt, which="first")
    end_time = pm.findKeyframe(pelvis_jnt, which="last")
    time_range = [start_frame, end_time]
    pm.setCurrentTime(start_frame)

    pelvis_loc = pm.spaceLocator(name="pelvis_Transform")
    root_loc = pm.spaceLocator(name="root_Transform")

    pelvis_cons_node = pm.parentConstraint(pelvis_jnt, pelvis_loc)
    pm.bakeResults(pelvis_loc, simulation=True, time=time_range)
    pm.delete(pelvis_cons_node)

    pm.parentConstraint(pelvis_loc, pelvis_jnt)

    root_loc.setParent(pelvis_loc)

    root_loc.setMatrix(root_pelvis_matrix)

    pm.parentConstraint(root_loc, root_jnt)
    pm.bakeResults(root_jnt, pelvis_jnt, simulation=True, time=time_range)
    pm.delete(pelvis_loc, root_loc)


if __name__ == "__main__":
    pelvis_jnt = nt.Joint("Bip001")
    root_jnt = nt.Joint("root")

    pelvis_jnt_wmatrix = pelvis_jnt.getMatrix(worldSpace=True)  # 获得胯骨骼世界矩阵
    root_jnt_wmatrix = root_jnt.getMatrix(worldSpace=True)  # 获得根骨骼世界矩阵（其实是个单位矩阵）
    pelvis_jnt_invers_wmatrix = pelvis_jnt_wmatrix.inverse()  # 胯骨骼世界矩阵求逆得到胯骨骼世界逆矩阵
    root_pelvis_matrix = root_jnt_wmatrix * pelvis_jnt_invers_wmatrix  # 根骨骼世界矩阵 左乘 胯骨骼世界逆矩阵 得到根骨骼到胯骨骼的 变换矩阵。

    '''
    # 其实这个值就是胯骨骼的世界逆矩阵，任何矩阵左乘单位矩阵，还是原来矩阵。
    root_pelvis_matrix = dt.Matrix(
        [
            [0.02043346792186473, 0.9979952200193409, 0.05990003511879664, 0.0],
            [-0.7260502627398266, 0.056000933000639685, -0.6853575063267978, 0.0],
            [-0.6873379731719432, -0.029486205615589286, 0.7257389849761965, 0.0],
            [45.067126241324154, 17.19906457141437, -301.9274085628932, 1.0],
        ]
    )
    '''
    loco_anim2root_anim(pelvis_jnt, root_jnt, root_pelvis_matrix)
