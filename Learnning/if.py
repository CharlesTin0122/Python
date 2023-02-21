#案例1
a = 123
b = 124
if a > b:
    print("a>b")
elif a < b:
    print("a<b")
else:
    print("a=b")

#案例2
age1 = 20
age2 = 17
if (age1 >= 18) and (age2 >= 18):
    print("OK")
else:
    print("No")

#案例3
age1 = 20
age2 = 17
if (age1 >= 18) or (age2 >= 18):
    print("OK")
else:
    print("No")

#案例4
polyCube = ['cube1',[0.1,5.2,3.7],8,12,6,'lambert1']
if "cube1" in polyCube:
    print("Find Item!")
else:
    print("Not Found!")

#案例5
import pymel.core as pm

selList = pm.ls(sl=True)

cubePre = "pCube"
sphPre = "pSphere"

for sel in selList:
    name = sel.name()
    if name[:-1]==cubePre:
        sel.setParent("CubeGrp")
    elif name[:-1]==sphPre:
        sel.setParent("SphereGrp")