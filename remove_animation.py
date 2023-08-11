# -*- coding: utf-8 -*-
"""
@FileName      : remove_animation.py
@DateTime      : 2023/08/11 14:35:20
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
"""
import pymel.core as pm


def deleteConnection(plug):
    """
        Deletes the connection of the given plug.
        Parameters:
            plug (str): The plug to delete the connection for.
        Returns:
            None
    """
    # 如果接口是连接的目标，则返回 true，否则返回 false。参数isDestination：是连接目标
    if pm.connectionInfo(plug, isDestination=True):
        # 获取确切目标接口，如果没有这样的连接，则返回None。
        plug = pm.connectionInfo(plug, getExactDestination=True)
        readOnly = pm.ls(plug, readOnly=True)
        # 如果该属性为只读
        if readOnly:
            # 获取连接的源接口
            source = pm.connectionInfo(plug, sourceFromDestination=True)
            # 断开源接口和目标接口
            pm.disconnectAttr(source, plug)
        else:
            # 如果不为只读，则删除目标接口
            # inputConnectionsAndNodes: 如果目标接口为只读，则不会删除
            pm.delete(plug, inputConnectionsAndNodes=True)


if __name__ == "__main__":
    # 获取选择列表
    sel_list = pm.selected()
    # 遍历选择列表
    for obj in sel_list:
        # 列出可动画属性
        attrs = obj.listAnimatable()
        # 遍历可动画属性
        for attr in attrs:
            # 断开动画连接
            deleteConnection(f"{attr}")
