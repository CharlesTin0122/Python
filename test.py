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

sel_mesh = pm.selected()[0]
sel_shape = sel_mesh.getShape()
assert isinstance(sel_shape, pm.nodetypes.Mesh)
sel_faces = sel_shape.faces
sel_deges = sel_shape.edges
sel_vtxs = sel_shape.vtx

for vtx in sel_vtxs:
    raySource = vtx.getPosition()
    vtx_normal = vtx.getNormal()
    rayDirection = raySource + vtx_normal * 1000000
    # 此函数是pm.nodetypes.Mesh类的方法，确定给定射线是否与此多边形相交，如果是，则返回交点。交点将按照距离射线源最近的点的顺序排列
    # 四个参数：1.射线源：点，2.射线方向：向量，3.容差：浮点，1e-10=1*10^-10，4.空间：‘transform’，‘preTransform’，‘object’，‘world’
    # 返回值：(bool, Point list, int list)
    intersect_point = sel_shape.intersect(
        raySource, rayDirection, tolerance=1e-10, space="object"
    )
