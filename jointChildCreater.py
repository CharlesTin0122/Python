import pymel.core as pm
#选择骨骼
jnt = pm.selected()[0]
#复制骨骼为子骨骼并重命名
jnt_add = pm.duplicate(jnt,name='{}_c'.format(jnt),parentOnly=True)[0]
#设置子骨骼父子关系
pm.parent(jnt_add,jnt)
#获取蒙皮节点
skin_cluster = pm.listConnections(jnt, type='skinCluster')[0]
#将子骨骼添加到蒙皮节点
pm.skinCluster(skin_cluster, edit=True, addInfluence=jnt_add)
#选择父骨骼蒙皮影响的点
pm.skinCluster(skin_cluster, edit=True, selectInfluenceVerts=jnt)
#传递父骨骼的蒙皮权重到子骨骼
pm.skinPercent(skin_cluster, transformMoveWeights=[jnt, jnt_add])