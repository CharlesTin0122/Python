# -*- coding: utf-8 -*-
# @FileName :  maya_api_2.0_vector.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/25 11:02
# @Software : PyCharm
# Description:
import math
import pymel.core as pm
import pymel.core.datatypes as dt
import pymel.core.nodetypes as nt

# get vector
obj = nt.Transform("locator1")
vec = obj.getTranslation(ws=True)
# get components
x = vec.x
y = vec.y
z = vec.z
print(x, y, z)
# set components
vec.x = 0
vec.y = 0
vec.z = 1
print(vec)
# add vectors
other_vec = dt.Vector(1, 0, 0)
added_vec = vec + other_vec
print(added_vec)
# subtract vectors
subtracted_vec = vec - other_vec
print(subtracted_vec)
# multiply vectors
multiplied_vec = vec * 2
print(multiplied_vec)
# get vector length
length = vec.length()
print(length)
# get vector distance
distance = vec.distanceTo(other_vec)
print(distance)
# projection On to 投影到
projection_vec = vec.projectionOnto(other_vec)
# get normalized vector
vec_normalized1 = vec.normal()  # 返回一个向量归一化副本
vec.normalize()  # 直接修改向量为归一化向量
print(vec_normalized1)
# dot product
dot_product = vec.dot(other_vec)
print(dot_product)
# cross product
cross_product1 = vec ^ other_vec
cross_product2 = vec.cross(other_vec)
print(cross_product1, cross_product2)
# get angle between vectors
angle = math.degrees(vec.angle(other_vec))  # angle（）获得两个向量之间的弧度，degrees（）将弧度转化为角度。
print(angle)
# rotate by vector
radians = dt.Vector(math.radians(90), 0, 0)  # math.radians将角度转化为弧度，得到一个弧度向量radians
rotateBy_vec_a = vec.rotateBy(radians)  # 使向量vec按照弧度向量radians旋转（x轴旋转90°）
rotateBy_vec_b = vec.rotateBy(
    dt.Vector.yAxis, math.radians(90)
)  # 也可以只选择一个轴进行旋转，YAxis意为Y轴
print(rotateBy_vec_a, rotateBy_vec_b)
# rotate to vector
rotateTo_vec = vec.rotateTo(other_vec)  # 返回的是一个四元数
