# -*- coding: utf-8 -*-
'''
@FileName      : test.py
@DateTime      : 2023/08/29 10:18:49
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
'''
import pymel.core as pm

sel_mesh = pm.selected()[0]
sel_shape = sel_mesh.getShape()
assert isinstance(sel_shape, pm.nodetypes.Mesh)
sel_faces = sel_shape.faces
sel_deges = sel_shape.edges
sel_vtxs = sel_shape.vtx
sel_normals = sel_shape.getNormals()
print(sel_faces,)
sel_shape.intersect()


'''
intersect(raySource, rayDirection, tolerance=1e-10, space='preTransform')
Determines whether the given ray intersects this polygon and if so, returns the points of intersection. The points of intersection will be in order of closest point to the raySource.

Parameters:	
raySource : Point
Starting point for the ray

rayDirection : Vector
Direction of the ray

tolerance : float
Tolerance used in intersection calculation

space : Space.Space
specifies the coordinate system for this operation

values: ‘transform’, ‘preTransform’, ‘object’, ‘world’

Return type:	
(bool, Point list, int list)

Derived from api method maya.OpenMaya.MSpace.intersect
'''
