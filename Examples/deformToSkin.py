import pymel.core as pm

# 创建环境
pm.polySphere(n='pSphere1')
pm.select(d=True)

for i in [0, 1, 2]:
    pm.joint()
    pm.select(d=True)
pm.move('joint2', 0, 1, 0)
pm.move('joint3', 0, -1, 0)

pm.select('pSphere1')
lat = pm.lattice(dv=(2, 3, 2), oc=True)

jointList = ['joint1', 'joint2', 'joint3']
pm.skinCluster(jointList, lat)

# 获取模型和点的信息
pm.select('pSphere1')
geo = pm.selected()
allVtxs = pm.ls('{}.vtx[*]'.format(geo[0]), fl=True)
vtxsDefPos = [pos.getPosition() for pos in allVtxs]
# 获取骨骼信息并通过移动骨骼获取点之间的位移差值作为权重
pm.select('joint1', 'joint2', 'joint3')
jointList = pm.selected()
allWeights = []
for jnt in jointList:
    jnt.tx.set(jnt.tx.get() + 1.0)
    moveVtxPos = map(lambda x: x[0] - x[1], zip([pos.getPosition() for pos in allVtxs], vtxsDefPos))
    jntWeightVal = [vec.length() for vec in moveVtxPos]
    jnt.tx.set(jnt.tx.get() - 1.0)
    allWeights.append(jntWeightVal)

# 移除变形
pm.setAttr("ffd1.envelope", 0)
# 创建多余骨骼以储存残余废权重
pm.select(d=True)
if not pm.objExists('otherWeights_jnt'):
    otherWeightsjnt = pm.joint(n='otherWeights_jnt')
jointList.append(otherWeightsjnt)
# 蒙皮并设置位移差值为蒙皮权重
geoSkinCluster = pm.skinCluster(jointList, geo)
pm.skinPercent(geoSkinCluster, allVtxs, transformValue=(jointList[-1], 1.0))

for j in range(len(jointList[:-1])):
    for i in range(len(allVtxs)):
        pm.skinPercent(geoSkinCluster, allVtxs[i], transformValue=(jointList[j], allWeights[j][i]))

    jointList[j].liw.set(1)
#	pm.setAttr('{}.liw'.format(jointList[j]),1) 两种方法都可以

# 移除废权重
pm.skinPercent(geoSkinCluster, geo, pruneWeights=0.1)
