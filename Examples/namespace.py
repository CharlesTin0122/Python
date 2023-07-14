import pymel.core as pm

# 创建选择物体列表
pm.select("Root", hi=True)
obj_list = pm.selected()
# 创建空间名称
ns = "asd"
pm.namespace(add=ns)
# 遍历选择列表，并给骨骼物体添加空间名称
for obj in obj_list:
    if pm.objectType(obj) == "joint":
        pm.rename(obj, "{}:{}".format(ns, obj))
    else:
        continue
# 删除空间名称
pm.namespace(rm=ns, mergeNamespaceWithRoot=True)
