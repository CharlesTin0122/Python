# -*- coding: utf-8 -*-
"""
@FileName    :   matrix_constrain.py
@DateTime    :   2023/06/13 14:19:39
@Author  :   Tian Chao
@Contact :   tianchao0533@163.com
"""

import maya.api.OpenMaya as om


# 定义 mgear_matrixConstraint 类
class MgearMatrixConstraint(om.MPxNode):
    # 定义节点类型和标识符
    kNodeName = "mgear_matrixConstraint"
    kNodeId = om.MTypeId(0x00000001)

    # 定义输入和输出属性
    inMatrix = om.MObject()
    inRotateOffset = om.MObject()
    inParentInverseMatrix = om.MObject()
    inInitialMatrix = om.MObject()
    outTranslate = om.MObject()
    outRotate = om.MObject()
    outScale = om.MObject()
    outShear = om.MObject()

    def __init__(self):
        super(MgearMatrixConstraint, self).__init__()

    @staticmethod
    def creator():
        return MgearMatrixConstraint()

    @staticmethod
    def initialize():
        # 创建输入和输出属性
        matrix_attr = om.MFnMatrixAttribute()
        numeric_attr = om.MFnNumericAttribute()

        # 输入属性初始化
        MgearMatrixConstraint.inMatrix = matrix_attr.create("inMatrix", "inm")
        matrix_attr.setWritable(True)
        matrix_attr.setReadable(True)
        matrix_attr.setKeyable(True)

        MgearMatrixConstraint.inRotateOffset = numeric_attr.create(
            "inRotateOffset", "inro", om.MFnNumericData.k3Double
        )
        numeric_attr.setWritable(True)
        numeric_attr.setReadable(True)
        numeric_attr.setKeyable(True)

        MgearMatrixConstraint.inParentInverseMatrix = matrix_attr.create(
            "inParentInverseMatrix", "inpm"
        )
        matrix_attr.setWritable(True)
        matrix_attr.setReadable(True)
        matrix_attr.setKeyable(True)

        MgearMatrixConstraint.inInitialMatrix = matrix_attr.create(
            "inInitialMatrix", "ini"
        )
        matrix_attr.setWritable(True)
        matrix_attr.setReadable(True)
        matrix_attr.setKeyable(True)

        # 输出属性初始化
        MgearMatrixConstraint.outTranslate = numeric_attr.create(
            "outTranslate", "ot", om.MFnNumericData.k3Double
        )
        numeric_attr.setWritable(False)
        numeric_attr.setReadable(True)
        numeric_attr.setStorable(False)

        MgearMatrixConstraint.outRotate = numeric_attr.create(
            "outRotate", "or", om.MFnNumericData.k3Double
        )
        numeric_attr.setWritable(False)
        numeric_attr.setReadable(True)
        numeric_attr.setStorable(False)

        MgearMatrixConstraint.outScale = numeric_attr.create(
            "outScale", "os", om.MFnNumericData.k3Double
        )
        numeric_attr.setWritable(False)
        numeric_attr.setReadable(True)
        numeric_attr.setStorable(False)

        MgearMatrixConstraint.outShear = numeric_attr.create(
            "outShear", "os", om.MFnNumericData.k3Double
        )
        numeric_attr.setWritable(False)
        numeric_attr.setReadable(True)
        numeric_attr.setStorable(False)

        # 添加属性到节点
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.inMatrix)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.inRotateOffset)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.inParentInverseMatrix)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.inInitialMatrix)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.outTranslate)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.outRotate)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.outScale)
        MgearMatrixConstraint.addAttribute(MgearMatrixConstraint.outShear)

        # 设置属性依赖关系
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inMatrix, MgearMatrixConstraint.outTranslate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inMatrix, MgearMatrixConstraint.outRotate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inMatrix, MgearMatrixConstraint.outScale
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inMatrix, MgearMatrixConstraint.outShear
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inRotateOffset, MgearMatrixConstraint.outTranslate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inRotateOffset, MgearMatrixConstraint.outRotate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inRotateOffset, MgearMatrixConstraint.outScale
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inRotateOffset, MgearMatrixConstraint.outShear
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inParentInverseMatrix,
            MgearMatrixConstraint.outTranslate,
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inParentInverseMatrix, MgearMatrixConstraint.outRotate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inParentInverseMatrix, MgearMatrixConstraint.outScale
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inParentInverseMatrix, MgearMatrixConstraint.outShear
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inInitialMatrix, MgearMatrixConstraint.outTranslate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inInitialMatrix, MgearMatrixConstraint.outRotate
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inInitialMatrix, MgearMatrixConstraint.outScale
        )
        MgearMatrixConstraint.attributeAffects(
            MgearMatrixConstraint.inInitialMatrix, MgearMatrixConstraint.outShear
        )

    def compute(self, plug, data):
        if (
            plug == MgearMatrixConstraint.outTranslate
            or plug == MgearMatrixConstraint.outRotate
            or plug == MgearMatrixConstraint.outScale
            or plug == MgearMatrixConstraint.outShear
        ):
            # 获取输入属性的值
            in_matrix_data = data.inputValue(MgearMatrixConstraint.inMatrix)
            in_rotate_offset_data = data.inputValue(
                MgearMatrixConstraint.inRotateOffset
            )
            in_parent_inverse_matrix_data = data.inputValue(
                MgearMatrixConstraint.inParentInverseMatrix
            )
            in_initial_matrix_data = data.inputValue(
                MgearMatrixConstraint.inInitialMatrix
            )

            in_matrix = in_matrix_data.asMatrix()
            in_rotate_offset = in_rotate_offset_data.asDouble3()
            in_parent_inverse_matrix = in_parent_inverse_matrix_data.asMatrix()
            in_initial_matrix = in_initial_matrix_data.asMatrix()

            # 进行计算操作，生成输出的变换属性值
            # ...

            # 设置输出属性的值
            out_translate_handle = data.outputValue(MgearMatrixConstraint.outTranslate)
            out_rotate_handle = data.outputValue(MgearMatrixConstraint.outRotate)
            out_scale_handle = data.outputValue(MgearMatrixConstraint.outScale)
            out_shear_handle = data.outputValue(MgearMatrixConstraint.outShear)

            out_translate_handle.setDouble3(...)
            out_rotate_handle.setDouble3(...)
            out_scale_handle.setDouble3(...)
            out_shear_handle.setDouble3(...)

            # 标记输出属性已更新
            out_translate_handle.setClean()
            out_rotate_handle.setClean()
            out_scale_handle.setClean()
            out_shear_handle.setClean()


# 注册节点
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerNode(
            MgearMatrixConstraint.kNodeName,
            MgearMatrixConstraint.kNodeId,
            MgearMatrixConstraint.creator,
            MgearMatrixConstraint.initialize,
        )
    except:
        om.MGlobal.displayError(
            "Failed to register node: {}".format(MgearMatrixConstraint.kNodeName)
        )


# 反注册节点
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterNode(MgearMatrixConstraint.kNodeId)
    except:
        om.MGlobal.displayError(
            "Failed to unregister node: {}".format(MgearMatrixConstraint.kNodeName)
        )
