#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/04/18 13:35
# @Author  : nb
"""
import creatjoints
creatjoints.createJointTools()
"""

import math
import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMaya as om
from collections import defaultdict


def analyze_and_get_extremum_vertices(mesh):
    normal_counts = defaultdict(list)
    vertices = cmds.ls(mesh + ".vtx[*]", fl=True)
    for vtx in vertices:
        normal_count = len(cmds.polyNormalPerVertex(vtx, q=1, x=True))
        normal_counts[normal_count].append(vtx)
    extremum_key = (
        max(normal_counts.keys())
        if len(normal_counts[min(normal_counts.keys())]) > len(vertices) / 2
        else min(normal_counts.keys())
    )
    return normal_counts[extremum_key]


def calculate_distance(a, b):
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def calculate_edge_threshold(extremum_vertices):
    mesh = extremum_vertices[0].split(".")[0]
    edge_lengths = {}
    for face in cmds.ls(mesh + ".f[*]", fl=1):
        faceToVertexValues = cmds.polyInfo(face, faceToVertex=1)
        vertex_indices_str = (
            faceToVertexValues[0].strip().replace("FACE ", "").strip().split()[1:]
        )
        vertex_positions = [
            cmds.xform(mesh + ".vtx[" + vtx + "]", q=True, ws=True, t=True)
            for vtx in vertex_indices_str
        ]
        max_dist = max(
            calculate_distance(pos1, pos2)
            for pos1 in vertex_positions
            for pos2 in vertex_positions
            if pos1 != pos2
        )
        edge_lengths[face] = max_dist

    total_distance = sum(edge_lengths.values())
    threshold = total_distance / len(edge_lengths) if edge_lengths else 0
    return threshold


def cluster_points_by_threshold(extremum_vertices):
    threshold = calculate_edge_threshold(extremum_vertices) * 2
    if len(extremum_vertices) > 1:
        first_vertex_pos = cmds.xform(extremum_vertices[0], q=1, t=1)
        distances_dict = {
            vtx: calculate_distance(first_vertex_pos, cmds.xform(vtx, q=1, t=1))
            for vtx in extremum_vertices[1:]
        }
        sorted_data = sorted(distances_dict.items(), key=lambda x: x[1])
        near_points, far_points = [], []
        for vtx_name, distance in sorted_data:
            if distance <= threshold:
                near_points.append(vtx_name)
            else:
                far_points.append(vtx_name)
        group_to_select = (
            near_points if near_points else far_points if far_points else []
        )
    else:
        group_to_select = extremum_vertices
    return group_to_select, threshold * 2


def get_soft_selection_weights():
    selected_vertices_weights = {}
    selected_objects = cmds.ls(sl=True)
    dag_path_parts = selected_objects[0].split(".")
    rich_selection_object = om.MRichSelection()
    om.MGlobal.getRichSelection(rich_selection_object)
    selection_list = om.MSelectionList()
    rich_selection_object.getSelection(selection_list)
    mesh_dag_path = om.MDagPath()
    component_mobject = om.MObject()
    selection_list.getDagPath(0, mesh_dag_path, component_mobject)
    component_fn = om.MFnSingleIndexedComponent(component_mobject)
    for index in range(component_fn.elementCount()):
        vertex_weight_value = component_fn.weight(index)
        vertex_index = component_fn.element(index)
        vertex_influence = vertex_weight_value.influence()
        vertex_name = (dag_path_parts[0] + ".vtx[%d]") % vertex_index
        selected_vertices_weights[vertex_name] = vertex_influence
    sorted_lattice_weights = sorted(
        selected_vertices_weights.items(), key=lambda x: x[1], reverse=True
    )
    return sorted_lattice_weights


def configureSoftSelection():
    cmds.ResetSoftSelectOptions()
    cmds.softSelect(e=1, softSelectCurve="0,1,0,1,0,1,1", softSelectEnabled=True)
    cmds.softSelect(softSelectFalloff=1, e=1)


def adjustSoftSelection(group_to_select, threshold):
    cmds.select(group_to_select)
    cmds.softSelect(e=True, softSelectDistance=threshold)
    while len(cmds.ls(group_to_select[0].split(".")[0] + ".vtx[*]", fl=1)) != len(
        get_soft_selection_weights()
    ):
        cmds.softSelect(
            softSelectDistance=cmds.softSelect(softSelectDistance=1, q=1) * 1.05, e=True
        )
    return get_soft_selection_weights()


def process_and_calculate_average(sorted_lattice_weights, decimal_places=2):
    grouped_points = {}
    for vtx_info in sorted_lattice_weights:
        vertex, distance = vtx_info
        rounded_distance = round(distance, decimal_places)
        if rounded_distance not in grouped_points:
            grouped_points[rounded_distance] = [vertex]
        else:
            grouped_points[rounded_distance].append(vertex)

    total_vertices_count = sum(len(vertices) for vertices in grouped_points.values())
    average_split_counts = total_vertices_count / len(grouped_points)
    return average_split_counts, grouped_points


def draw_centers_curve(
    split_count,
    sorted_lattice_weights,
    group_to_select,
    curve_suffix="_meshCurve",
    rebuildCurveCount=2,
):
    curves, all_vertices, nums = (
        [],
        [s[0] for s in sorted_lattice_weights],
        int(split_count),
    )
    sub_lists_of_vertices = [
        all_vertices[i : i + nums] for i in range(0, len(all_vertices), nums)
    ]
    sub_lists_centers = []
    for sublist in sub_lists_of_vertices:
        sublist_positions = [cmds.xform(vtx, q=1, t=1, ws=1) for vtx in sublist]
        center_coordinates = [
            sum(coord) / len(sublist) for coord in zip(*sublist_positions)
        ]
        sub_lists_centers.append(center_coordinates)
    curve_name = group_to_select[0].split(".")[0] + curve_suffix
    cmds.curve(
        n=curve_name,
        p=sub_lists_centers,
        k=[c for c in range(len(sub_lists_centers))],
        d=1,
    )

    smoothV = cmds.floatField("INTField_grp_smooth_Curve", q=1, v=1)
    pm.mel.modifySelectedCurves("smooth", smoothV, 0)

    spans = float(len(sub_lists_centers) / rebuildCurveCount)
    cmds.rebuildCurve(
        rt=0, ch=0, end=1, d=5, kr=0, s=spans, kcp=0, tol=0.01, kt=0, rpo=1, kep=1
    )

    curves.append(curve_name)
    return curves


def draw_centerline():
    curves = []
    selected_meshs = cmds.ls(sl=1)
    decimal_places_Value = cmds.intField("INTField_grp", q=1, v=1)

    if ".vtx" in selected_meshs[0]:
        sorted_lattice_weights = get_soft_selection_weights()
        split_count, grouped_points = process_and_calculate_average(
            sorted_lattice_weights, decimal_places=decimal_places_Value
        )
        curve = draw_centers_curve(
            split_count,
            sorted_lattice_weights,
            selected_meshs,
            curve_suffix="_meshCurve",
            rebuildCurveCount=2,
        )
        curves.append(curve[0])
    elif ".e" in selected_meshs[0]:
        if len(selected_meshs) != 2:
            curve1 = creatJoints1(selected_meshs)
            curves.append(curve1)
        else:
            curve1 = creatJoints(selected_meshs)
            curves.append(curve1)
    elif cmds.objectType(selected_meshs[0]) == "joint":
        InsertJnt()
    else:
        configureSoftSelection()
        for mesh in selected_meshs:
            extremum_vertices = analyze_and_get_extremum_vertices(mesh)
            group_to_select, threshold = cluster_points_by_threshold(extremum_vertices)
            sorted_lattice_weights = adjustSoftSelection(group_to_select, threshold)
            split_count, grouped_points = process_and_calculate_average(
                sorted_lattice_weights, decimal_places=decimal_places_Value
            )
            curve = draw_centers_curve(
                split_count,
                sorted_lattice_weights,
                group_to_select,
                curve_suffix="_meshCurve",
                rebuildCurveCount=2,
            )
            curves.append(curve[0])
    return curves


def creat_joints_on_curves(curves, ifDeleteCurve=True):
    jntNums = num_balls = cmds.intSliderGrp("slider_control", query=True, value=True)
    for curve in curves:
        isNurbsCircle = len(cmds.ls(curve + ".cv[*]", fl=True)) != cmds.getAttr(
            curve + ".spans"
        )
        joint_positions, pointOnCurveInfos = [], []
        for l in range(jntNums):
            parameter = 0 if l == 0 else l / float(jntNums - isNurbsCircle)
            pointOnCurveInfo = cmds.createNode("pointOnCurveInfo")
            cmds.setAttr("%s.turnOnPercentage" % pointOnCurveInfo, 1)
            cmds.setAttr("%s.parameter" % pointOnCurveInfo, parameter)
            cmds.connectAttr(
                "%s.worldSpace[0]" % curve, "%s.inputCurve" % pointOnCurveInfo, f=1
            )
            joint_positions.append(cmds.getAttr("%s.position" % pointOnCurveInfo))
            pointOnCurveInfos.append(pointOnCurveInfo)
        joints = [cmds.joint(p=pos[0]) for pos in joint_positions]
        cmds.select(joints[0])
        cmds.joint(zso=1, ch=1, e=1, oj="xyz", secondaryAxisOrient="yup")
        orient_attrs = ["jointOrientX", "jointOrientY", "jointOrientZ"]
        [cmds.setAttr(joints[-1] + "." + attr, 0) for attr in orient_attrs]
        pm.mel.searchReplaceNames("joint", curve[:-10] + "_Joint", "hierarchy")
    cmds.delete(pointOnCurveInfos)
    if ifDeleteCurve:
        cmds.delete(curves)


def createJointTools():
    window_name = "CreateJointTools"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    cmds.window(window_name, title=window_name, tlb=1, resizeToFitChildren=True)
    form_layout = cmds.formLayout(numberOfDivisions=20)
    row_layout = cmds.rowLayout(numberOfColumns=4, adjustableColumn=1)
    slider_control = cmds.intSliderGrp(
        "slider_control",
        label="Joints Count:",
        field=True,
        minValue=0,
        maxValue=50,
        value=0,
        dragCommand=lambda *args: update_sphere_count(args),
        changeCommand=lambda *args: update_sphere_count(args),
        parent=row_layout,
    )
    Intf = cmds.intField("INTField_grp", width=25, height=25, v=1, parent=row_layout)
    cmds.floatField(
        "INTField_grp_smooth_Curve", width=40, height=25, pre=2, v=1, parent=row_layout
    )
    cmds.iconTextButton(
        style="iconOnly",
        image1="kinReroot.png",
        label="spotlight",
        c="cmds.RerootSkeleton()",
    )
    cmds.formLayout(
        form_layout,
        edit=True,
        attachForm=[
            (row_layout, "top", 3),
            (row_layout, "left", -65),
            (row_layout, "right", 3),
            (row_layout, "bottom", 3),
        ],
    )
    cmds.showWindow(window_name)


def update_sphere_count(*args):
    existing_spheres = cmds.ls("*_Joint*") + cmds.ls("*meshCurve")
    for i in existing_spheres:
        if cmds.ls(i):
            if cmds.objectType(cmds.ls(sl=1)[0]) != "joint":
                cmds.delete(existing_spheres)
    if cmds.objectType(cmds.ls(sl=1)[0]) == "joint":
        jnts = cmds.ls(cmds.ls(sl=1)[0] + "_insert_*")
        if jnts != []:
            joints = cmds.ls(sl=1)
            cmds.parent(
                cmds.listRelatives(jnts[-1], c=1)[0],
                cmds.listRelatives(jnts[0], p=1)[0],
            )
            cmds.delete(jnts)
            cmds.select(joints)
    meshs = cmds.ls(sl=1)
    curves = draw_centerline()
    cmds.select(meshs)
    num_balls = int(cmds.intSliderGrp("slider_control", query=True, value=True))
    if num_balls != 0:
        if curves != []:
            creat_joints_on_curves(curves)
    cmds.select(meshs)


def centerPos(vtxs):
    axial = [[], [], []]
    for vtx in vtxs:
        for a in range(3):
            axial[a].append(cmds.pointPosition(vtx)[a])
    axial = (
        sum(axial[0]) / len(vtxs),
        sum(axial[1]) / len(vtxs),
        sum(axial[2]) / len(vtxs),
    )
    return axial


def getCenterPosition():
    positions = []
    cmds.SelectEdgeRingSp()
    for i in cmds.ls(sl=1, fl=1):
        cmds.select(i)
        cmds.polySelectSp(loop=1)
        pm.mel.PolySelectConvert(3)
        vtxs = cmds.ls(sl=1, fl=1)
        position = centerPos(vtxs)
        positions.append(position)
    cmds.select(cl=1)
    return positions


def reorderPosition():
    minDis, positions = {}, getCenterPosition()
    for i in range(len(positions)):
        minDis[i] = calculate_distance([0, 0, 0], positions[i])
    return positions, sorted(minDis.items(), key=lambda x: x[1], reverse=True)


def creatJoints(selected_meshs, curve_suffix="_meshCurve"):
    curve_name = selected_meshs[0].split(".")[0] + curve_suffix
    positions, reorderPositions = reorderPosition()
    startVtx = positions[max(reorderPositions)[0]]
    positions.remove(startVtx)
    distances = [calculate_distance(startVtx, point) for point in positions]
    distance_pairs = [
        (point, distance) for point, distance in zip(positions, distances)
    ]
    sorted_pairs = sorted(distance_pairs, key=lambda x: x[1])
    sorted_positions = [pair[0] for pair in sorted_pairs]
    sorted_positions.insert(0, startVtx)
    cmds.curve(
        n=curve_name,
        p=sorted_positions,
        k=[c for c in range(len(sorted_positions))],
        d=1,
    )
    smoothV = cmds.floatField("INTField_grp_smooth_Curve", q=1, v=1)
    pm.mel.modifySelectedCurves("smooth", smoothV, 0)
    return curve_name


def creatJoints1(selected_meshs, curve_suffix="_meshCurve"):
    curve_name = selected_meshs[0].split(".")[0] + curve_suffix
    cmds.polyToCurve(name=curve_name, conformToSmoothMeshPreview=1, degree=1, form=2)
    cmds.DeleteHistory()
    smoothV = cmds.floatField("INTField_grp_smooth_Curve", q=1, v=1)
    pm.mel.modifySelectedCurves("smooth", smoothV, 0)
    return curve_name


def InsertJnt():
    numOfjnt = cmds.intSliderGrp("slider_control", query=True, value=True)
    NumOfjnt = numOfjnt + 1
    if numOfjnt <= 0:
        pass
    else:
        jntObj0 = cmds.ls(sl=True)[0]
        jntObj1 = cmds.listRelatives(jntObj0, c=1)
        trOld = cmds.xform(jntObj1, q=1, translation=1)
        cmds.parent(jntObj1, world=1)
        for i in range(numOfjnt):
            I = i + 1
            RenameJnt = cmds.insertJoint(jntObj0)
            cmds.setAttr(RenameJnt + ".radius", cmds.getAttr(jntObj0 + ".radius"))
            insertTranslateNew = cmds.xform(
                RenameJnt, translation=[trOld[i] / (numOfjnt + 1) for i in range(3)]
            )
            cmds.rename(RenameJnt, jntObj0 + "_insert_" + str(numOfjnt - I))
        cmds.parent(jntObj1, jntObj0 + "_insert_" + str(numOfjnt - 1))
        cmds.select(jntObj0)
