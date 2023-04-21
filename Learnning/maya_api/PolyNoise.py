# -*- coding: utf-8 -*-
# @FileName :  PolyNoise.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/11 9:54
# @Software : PyCharm
# Description:
# 在执行python前 必须导入maya的一个模块 https://download.autodesk.com/us/maya/2010help/API/modules.html
# 因为maya命令库中不包含random, time等功能，所以我们要手动导入这些
import random
import time

import maya.OpenMaya as om
# 导入maya的命令库,这个是必须操作
import maya.cmds as cmds


# 创建功能函数 它的格式是def name(xxx,xxx): 然后回车缩进，缩进后的内容被这个函数执行
def arPolyNoise(geoObject, maxDisplacement):
    # 使用三个双引号来进行的注释
    """使用提供的“最大置换”（max displacement）将噪波应用于提供的几何体对象。"""
    # 实例化一个选择列表
    selection = om.MSelectionList()
    # 获取DagPath
    dagPath = om.MDagPath()
    try:
        # 在列表中添加物体
        selection.add(geoObject)
        # 添加DagPath
        selection.getDagPath(0, dagPath)
    except:
        raise
    # 添加噪波到模型的顶点
    try:
        # 初始化集合体迭代器
        geoIter = om.MItGeometry(dagPath)
        # 获取世界空间中所有顶点的位置
        pArray = om.MPointArray()
        geoIter.allPositions(pArray)
        # 偏移每个顶点
        for i in xrange(pArray.length()):
            # 计算随机的偏移大小
            displacement = om.MVector.one * random.random() * maxDisplacement
            # 三个轴向增加随机偏移
            pArray[i].x += displacement.x
            pArray[i].y += displacement.y
            pArray[i].z += displacement.z
        # 使用更改后的顶点应用到模型
        geoIter.setAllPositions(pArray)
        meshFn = om.MFnMesh(dagPath)
        # 更新模型曲面
        meshFn.updateSurface()
    except:
        raise


# 开始计时器
timeStart = time.clock()
# 创建一个球体并且添加噪声
sphere = cmds.polySphere(radius=1, subdivisionsX=200, subdivisionsY=200)
arPolyNoise(sphere[0], 0.02)
# 停止计时器
timeStop = time.clock()
# 输出运行时间
print('Execution time: %s seconds.' % (timeStop - timeStart))
