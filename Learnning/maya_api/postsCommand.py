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
class PostsCommand(OpenMayaMPx.MPxCommand):
    kPluginCmdName = "Posts"  # 命令名称

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)  # 调用MPxCommand构建函数
        self.dgModifier = OpenMaya.MDGModifier()  # 将MDGModifier实例化，用于命令的undo和redo
        self.height_ratio = None
        self.height = None
        self.radius = None
        self.nposts = None

    @staticmethod
    def cmd_creator():
        return OpenMayaMPx.asMPxPtr(PostsCommand())  # 用于将自定义的 Python 类转换为 Maya 所使用的 MPx 指针（MPxPtr）。

    def doIt(self, args):
        self.nposts = 5  # posts数量默认设为5
        self.radius = 0.5  # 默认半径为0.5
        self.height = 5.0  # 默认高度为5.0
        self.height_ratio = self.height / self.radius  # 创建高度半径比变量

        selection = OpenMaya.MSelectionList()  # 创建选择列表为空
        OpenMaya.MGlobal.getActiveSelectionList(selection)  # 获取当前场景所有选择的对象放入selection列表
        dag_path = OpenMaya.MDagPath()  # 创建dag路径变量
        curve_fn = OpenMaya.MFnNurbsCurve()  # 创建Nurbs曲线函数
        # 创建选择列表迭代器类,第一个参数为要迭代的对象列表，第二个参数为要迭代的对象类型为NurbsCurve，是个过滤器参数
        selection_iter = OpenMaya.MItSelectionList(selection, OpenMaya.MFn.kNurbsCurve)

        # 为曲线创建起始和结束参数，参数类型为double,Python中没有double类型，因此要使用OpenMaya.MScriptUtil()工具类来创建double类型
        """双精度浮点型(double)，此数据类型与单精度数据类型(float)相似，但精确度比float高，
        单精度浮点数(float)占4字节（32位）内存空间；双精度型(double)占8个字节（64位）内存空间，"""

        """创建了一个MScriptUtil类的实例，
        并使用它的createFromDouble()方法创建一个值为0的double类型,
        使用asDoublePtr()方法将此值存储为指向double的指针。"""

        # 创建一个MScriptUtil实例，用于执行Maya API中的一些实用功能。
        t_start_param = OpenMaya.MScriptUtil()
        # 使用MScriptUtil实例的createFromDouble()方法，创建一个double类型的值为0的参数。
        t_start_param.createFromDouble(0)
        # 使用MScriptUtil实例的asDoublePtr()方法，将创建的double参数转换为指向该参数的指针（double pointer）。
        t_start_ptr = t_start_param.asDoublePtr()
        # 曲线的结束值
        t_end_param = OpenMaya.MScriptUtil()
        t_end_param.createFromDouble(0)
        t_end_ptr = t_end_param.asDoublePtr()
        #
        while selection_iter.isDone() == 0:  # isDone()如果没有对象可以迭代了，返回True,如果有对象可以迭代，返回False。
            selection_iter.getDagPath(dag_path)  # 对迭代器里的对象获取DagPath，并存储到dag_path中
            curve_fn.setObject(dag_path)  #
            """OpenMaya.MFnNurbsCurve.getKnotDomain() 是用于获取NURBS曲线的节点域（knot domain）的方法。
            节点域是定义曲线参数范围的一对参数，通常表示为曲线上参数的最小值和最大值"""
            curve_fn.getKnotDomain(t_start_ptr, t_end_ptr)

            pt = OpenMaya.MPoint()  # 创建一个点的变量，可以获取他的位置信息
            start = OpenMaya.MScriptUtil(t_start_ptr).asDouble()  # start声明成double数据对象
            end = OpenMaya.MScriptUtil(t_end_ptr).asDouble()  # end声明成double数据对象
            t_iter = (end - start) / (self.nposts - 1)  # 结束的点减去开始的点除以段数减一，得到每段的量
            # 遍历每段曲线进行操作
            for i in range(0, self.nposts):
                # OpenMaya.MFnNurbsCurve().getPointAtParam(),用于获取曲线（NURBS 曲线）上指定参数位置处的点坐标
                # 该函数允许你在曲线上通过指定参数值来获取该参数位置处的点的坐标。
                curve_fn.getPointAtParam(start, pt, OpenMaya.MSpace.kWorld)
                pt.y += 0.5 * self.height
                start += t_iter
                # 利用OpenMaya.MDGModifier.commandToExecute存储命令
                self.dgModifier.commandToExecute(
                    f"cylinder -pivot {pt.x} {pt.y} {pt.z} -radius {self.radius} -heightRatio {self.height_ratio};"
                )
                self.dgModifier.commandToExecute("select -cl")
            selection_iter.next()  # 迭代器继续迭代
        self.redoIt()  # 执行命令

    def isUndoable(self):  # 是否可撤销
        return True

    def undoIt(self):  # 撤销
        self.dgModifier.undoIt()

    def redoIt(self):  # 重做
        self.dgModifier.doIt()


# Initialize the script plug-in
def initializePlugin(plugin):  # 注册命令
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        plugin_fn.registerCommand(
            PostsCommand.kPluginCmdName,
            PostsCommand.cmd_creator
        )
    except Exception as exc:
        raise sys.stderr.write(
            f"Failed to register command: {PostsCommand.kPluginCmdName}\n"
        ) from exc


# Uninitialize the script plug-in
def uninitializePlugin(plugin):  # 取消注册命令
    plugin_fn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        plugin_fn.deregisterCommand(PostsCommand.kPluginCmdName)
    except Exception as exc:
        raise sys.stderr.write(
            f"Failed to unregister command: {PostsCommand.kPluginCmdName}\n"
        ) from exc
