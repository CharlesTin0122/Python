polyCubeDict = {
    "name": "cube1",
    "position": [0.1, 5.2, 3.7],
    "points": 8,
    "edges": 12,
    "faces": 6,
    "material": "lambert1",
}  # 创建字典键值对

polyCubeDict["name"] = "cube2"  # 修改字典内容
polyCubeDict["hasUV"] = True  # 新增字典键值对
del polyCubeDict["faces"]  # 删除字典键值对

name = polyCubeDict["name"]
pos = polyCubeDict["position"]
mat = polyCubeDict["material"]
print(name)
print(pos)
print(mat)
print(polyCubeDict)
print(polyCubeDict.keys())  # 只打印键
print(polyCubeDict.values())  # 只打印值
print(polyCubeDict.items())  # 打印键和值
