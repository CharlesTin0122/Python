# 遍历 for循环

myStr = "hello world!"
for letter in myStr:
    print("the letter is:")
    print(letter)

print("the end")


myInt = [3, 1, 9, 7, 4, 6]
for i in range(len(myInt)):
    print(myInt[i])


import pymel.core as pm

selList = pm.ls(sl=True)
for i in range(len(selList)):
    pos = selList[i].getTranslation()
    selList[i].setTranslation([pos.x, pos.y + i, pos.z])
print(selList)


polyCubeDict = {
    "name": "cube1",
    "position": [0.1, 5.2, 3.7],
    "points": 8,
    "edges": 12,
    "faces": 6,
    "material": "lambert1",
}
for k, v in polyCubeDict.items():
    print("key:{},value:{}".format(k, v))


"""枚举循环"""
import pymel.core as pm

obj = pm.selected()
# 枚举
for index, data in enumerate(obj):
    print(index, data)
