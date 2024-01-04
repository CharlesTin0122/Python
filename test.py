# -*- coding: utf-8 -*-
"""
@FileName      : test.py
@DateTime      : 2023/08/29 10:18:49
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
"""
import pymel.core as pm


def create_joint_per_mesh(sel_obj: list):
    """为每个选中的模型在边界框(bounding box)中心创建一个骨骼

    Args:
        sel_obj (list): 模型列表

    Returns:
        list: 骨骼列表
    """
    jnt_list = []
    for obj in sel_obj:
        pm.select(cl=True)
        jnt = pm.joint(name=f"jnt_{obj}", position=obj.c.get())
        jnt_list.append(jnt)
    return jnt_list


if __name__ == "__main__":
    sel_obj1 = pm.selected()
    new_jnt = create_joint_per_mesh(sel_obj1)


def clean_mesh(obj_list: list):
    """清理蒙皮用模型：主要过程是：
    1.冻结变换
    2.删除构建历史
    3.还原旋转轴心至原点

    Args:
        obj_list (list): 要处理的模型文件列表,类型是Transform
    """
    for obj in obj_list:
        pm.makeIdentity(
            obj, apply=True, translate=1, rotate=1, scale=1, normal=0, preserveNormals=1
        )
        pm.delete(obj, constructionHistory=True)
        obj.rotatePivot.set(0, 0, 0)


if __name__ == "__main__":
    sel_objs = pm.selected()
    clean_mesh(sel_objs)
