# -*- coding: utf-8 -*-
"""
@FileName      : bake_euler_to_quaternion.py
@DateTime      : 2023/11/16 10:24:08
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
@Description   :
"""
import math
from maya.api.OpenMaya import MQuaternion, MEulerRotation
import pymel.core as pm
import pymel.core.datatypes as dt

# Use pymel
quat = dt.Quaternion(0.707, 0, 0, 0.707)
print(quat.asEulerRotation())
print(quat.asMatrix())

# Use pymel to get obj`s Quaternion
obj = pm.selected()[0]

euler_rot = obj.getRotation()
quat_rot = euler_rot.asQuaternion()
# or

quat_rot2 = obj.getRotation(quaternion=True)
print(quat_rot2.x, quat_rot2.y, quat_rot2.z, quat_rot2.w)
obj.setRotation(quat_rot2, quaternion=True, space="world")

dir_quat = [
    "I",
    "T",
    "__abs__",
    "__add__",
    "__call__",
    "__class__",
    "__coerce__",
    "__contains__",
    "__delattr__",
    "__delitem__",
    "__delslice__",
    "__dict__",
    "__dir__",
    "__div__",
    "__doc__",
    "__eq__",
    "__floordiv__",
    "__format__",
    "__ge__",
    "__getattribute__",
    "__getitem__",
    "__getnewargs__",
    "__getslice__",
    "__gt__",
    "__hash__",
    "__iadd__",
    "__idiv__",
    "__ifloordiv__",
    "__imod__",
    "__imul__",
    "__init__",
    "__init_subclass__",
    "__invert__",
    "__ipow__",
    "__isub__",
    "__iter__",
    "__itruediv__",
    "__le__",
    "__len__",
    "__lt__",
    "__melobject__",
    "__mod__",
    "__module__",
    "__mul__",
    "__ne__",
    "__neg__",
    "__neq__",
    "__new__",
    "__pos__",
    "__pow__",
    "__radd__",
    "__rdiv__",
    "__readonly__",
    "__reduce__",
    "__reduce_ex__",
    "__repr__",
    "__rfloordiv__",
    "__rmod__",
    "__rmul__",
    "__round__",
    "__rpow__",
    "__rsub__",
    "__rtruediv__",
    "__setattr__",
    "__setitem__",
    "__setslice__",
    "__sizeof__",
    "__slots__",
    "__str__",
    "__sub__",
    "__subclasshook__",
    "__swig_destroy__",
    "__truediv__",
    "__weakref__",
    "_cacheshape",
    "_checkaxis",
    "_checkindex",
    "_convert",
    "_data",
    "_defaultshape",
    "_deldata",
    "_delete",
    "_expandshape",
    "_extract",
    "_fitloop",
    "_formatloop",
    "_gauss_jordan",
    "_getRotate",
    "_getScale",
    "_getTranslate",
    "_getaxis",
    "_getdata",
    "_getindex",
    "_getitem",
    "_getncol",
    "_getnrow",
    "_getshape",
    "_inject",
    "_iterable_convert",
    "_ndim",
    "_setRotate",
    "_setScale",
    "_setTranslate",
    "_setdata",
    "_setncol",
    "_setnrow",
    "_setshape",
    "_shape",
    "_shapecheck",
    "_size",
    "_strip",
    "_toCompOrConvert",
    "_trimloop",
    "a00",
    "a01",
    "a02",
    "a03",
    "a10",
    "a11",
    "a12",
    "a13",
    "a20",
    "a21",
    "a22",
    "a23",
    "a30",
    "a31",
    "a32",
    "a33",
    "adjoint",
    "adjugate",
    "all",
    "any",
    "apicls",
    "append",
    "appended",
    "asEulerRotation",
    "asMatrix",
    "assign",
    "axisiter",
    "basis",
    "blend",
    "clamp",
    "className",
    "cnames",
    "cofactor",
    "col",
    "conjugate",
    "conjugateIt",
    "copy",
    "count",
    "data",
    "deepcopy",
    "deleted",
    "det",
    "det3x3",
    "det4x4",
    "diagonal",
    "dist",
    "distanceTo",
    "exp",
    "extend",
    "extended",
    "fill",
    "filled",
    "fit",
    "fitted",
    "flat",
    "formated",
    "gauss",
    "get",
    "getAxisAngle",
    "homogenize",
    "hstack",
    "hstacked",
    "identity",
    "imag",
    "index",
    "inv",
    "inverse",
    "invertIt",
    "isEquivalent",
    "isSingular",
    "is_square",
    "length",
    "linverse",
    "log",
    "matrix",
    "max",
    "min",
    "minor",
    "ncol",
    "ndim",
    "negateIt",
    "normal",
    "normalize",
    "normalizeIt",
    "nrow",
    "prod",
    "ravel",
    "real",
    "reduced",
    "reshape",
    "reshaped",
    "resize",
    "resized",
    "rinverse",
    "rotate",
    "row",
    "scale",
    "scaleIt",
    "setAxisAngle",
    "setToIdentity",
    "setToProduct",
    "setToXAxis",
    "setToYAxis",
    "setToZAxis",
    "shape",
    "size",
    "sqlength",
    "stack",
    "stacked",
    "strip",
    "stripped",
    "subiter",
    "sum",
    "this",
    "thisown",
    "tolist",
    "totuple",
    "trace",
    "translate",
    "transpose",
    "trim",
    "trimmed",
    "vstack",
    "vstacked",
    "w",
    "weighted",
    "x",
    "y",
    "z",
]
# Use Maya Python API 2.0
q = MQuaternion(0.707, 0, 0.707, 0)
q.normalizeIt()  # to normalize
print(q)
print(q.asEulerRotation())
e = MEulerRotation(
    math.radians(45), math.radians(60), math.radians(90), MEulerRotation.kXYZ
)
print(e)
print(e.asQuaternion())

# THis is our rotation, specified in degrees
rot = [45, 90, 0]
# This is our rotation order
rotOrder = MEulerRotation.kXYZ
# Create the MEulerRotation
euler = MEulerRotation(
    math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder
)
# Get the quaternion equivalent
quaternion = euler.asQuaternion()
# Access the components
print(quaternion.x, quaternion.y, quaternion.z, quaternion.w)
