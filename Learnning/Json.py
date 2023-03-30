#案例1

import json
'''
如果你要处理的是文件而不是字符串，你可以使用 json.dump() 和 json.load() 来编码和解码JSON数据
'''
data = {
    "abc": 123,
    "Path": "D:\Work_MobilGame\Test",
    "123": 1.0
}

#写入
with open("testttttt.json","w") as f:
    json.dump(data, f, indent=4)


#读取
with open("test.json", "r") as f:
    data = json.load(f)
print(data)

#案例2

import maya.cmds as mc
#创建一一对应列表
attrList = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ']
attrVal = [1.046,1.712,3.438,-14.464,15.652,50.186,1,1,1]
#将两个列表压缩成一一对应的元组列表
zipList = zip(attrList,attrVal)
#将一一对应的元组列表生成字典
data = dict(zipList)

import json
#设置保存路径和写入的变量
path = r'C:\Users\tianc\Documents\maya\2020\prefs\scripts\pSphere1.json'
jsonData = json.dumps(data)
#写入
with open(path,'w') as f:
	f.write(jsonData)
#读取
with open(path,'r') as f:
	sourceData = f.read()
#编码为maya可用
targetData = json.JSONDecoder().decode(sourceData)
#字典循环使用方法
for key,value in targetData.items():
	print(key,value)