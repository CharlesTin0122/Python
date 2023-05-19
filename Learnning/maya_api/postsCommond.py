# -*- coding: utf-8 -*-
# @FileName :  postsCommond.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/11 10:05
# @Software : PyCharm
# Description:
import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx


# command
class PostsCommond(OpenMayaMPx.MPxCommand):
    kPluginCmdName = "Posts"

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
        self.height = None
        self.radius = None
        self.nposts = None

    @staticmethod
    def cmd_creator():
        return OpenMayaMPx.asMPxPtr(PostsCommond())

    def doIt(self, args):
        self.nposts = 5  # posts数量默认设为5
        self.radius = 0.5  # 默认半径为0.5
        self.height = 5.0  # 默认高度为5.0
        height_ratio = self.height / self.radius  # 创建高度半径比变量

        selection = OpenMaya.MSelectionList()  # 创建选择列表为空
        OpenMaya.MGlobal.getActiveSelectionList(selection)  # 获取当前场景所有选择的对象放入selection列表
        dag_path = OpenMaya.MDagPath()  # 创建dag路径变量
        curve_fn = OpenMaya.MFnNurbsCurve()  # 创建Nurbs曲线函数
        # 创建选择列表迭代器类,第一个参数为要迭代的对象列表，第二个参数为要迭代的对象类型为NurbsCurve，是个过滤器参数
        selection_iter = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kNurbsCurve)

        # 为曲线创建起始和结束参数，参数类型为double,Python中没有double类型，因此要使用OpenMaya.MScriptUtil()工具类来创建double类型
        # 曲线的起始值
        t_start_param = OpenMaya.MScriptUtil()  # 创建MScriptUtil()工具类实例
        t_start_param.createFromDouble(0)  # 使用MScriptUtil()工具类的createFromDouble()方法来创建一个0的double类型
        t_start_ptr = t_start_param.asDoublePtr()  # 把他作为一个double的ptr的指针进行存储
        # 曲线的结束值
        t_end_param = OpenMaya.MScriptUtil()
        t_end_param.createFromDouble(0)
        t_end_ptr = t_start_param.asDoublePtr()

        while selection_iter.isDone() == 0:
            selection_iter.getDagPath(dag_path)
            curve_fn.setObject(dag_path)

            pt = OpenMaya.MPoint()
            start = OpenMaya.MScriptUtil(t_start_ptr).asDouble()
            end = OpenMaya.MScriptUtil(t_end_ptr).asDouble()
            t_iter = (end - start) / (self.nposts - 1)


# Initialize the script plug-in
def initialize_plugin(plugin):
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        plugin_fn.registerCommand(
            PostsCommond.kPluginCmdName, PostsCommond.cmd_creator
        )
    except Exception as exc:
        raise sys.stderr.write(
            f"Failed to register command: {PostsCommond.kPluginCmdName}\n"
        ) from exc


# Uninitialize the script plug-in
def uninitialize_plugin(plugin):
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PostsCommond.kPluginCmdName)
    except Exception as exc:
        raise sys.stderr.write(
            f"Failed to unregister command: {PostsCommond.kPluginCmdName}\n"
        ) from exc
