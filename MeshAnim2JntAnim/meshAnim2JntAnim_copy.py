import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import pymel.core as pm

time_start = pm.playbackOptions(q=True, min=True)
time_end = pm.playbackOptions(q=True, max=True)
current_time = pm.currentTime(time_start)

sel_list = OpenMaya.MSelectionList()
OpenMaya.MGlobal.getActiveSelectionList(sel_list)

sel_mesh = OpenMaya.MDagPath()
sel_list.getDagPath(0, sel_mesh)
sel_fn = OpenMaya.MFnMesh(sel_mesh)

mesh_vtxs = OpenMaya.MPointArray()
sel_fn.getPoints(mesh_vtxs)
OpenMaya.MGlobal.clearSelectionList()

mesh_dag = OpenMaya.MDagPath()
sel_list.getDagPath(0, mesh_dag)
mesh_RotatePivot = OpenMaya.MFnTransform(mesh_dag).rotatePivot(
    OpenMaya.MSpace.kWorld
)

root_jnt = OpenMayaAnim.MFnIkJoint()
root_jnt.create()
root_jnt.setName("root")
root_jnt.setTranslation(mesh_RotatePivot, OpenMaya.MSpace.kWorld)

jnt_list = []
for i in range(mesh_vtxs.length()):
    vtx_pos = mesh_vtxs[i]
    jnt_pnt = OpenMaya.MFnIkJoint()
    jnt_pnt.create(True)
    jnt_pnt.setName(f"jnt_{i}")
    jnt_pnt.setRadius(0.1)
    jnt_pnt.setTranslation(vtx_pos, OpenMaya.MSpace.kWorld)
    jnt_pnt.setParent(root_jnt)
    jnt_list.append(jnt_pnt)

for frame in range(int(time_start), int(time_end) + 1):
    current_time.setValue(frame)
    OpenMaya.MAnimControl.setCurrentTime(current_time)
    for i, vtx in enumerate(mesh_vtxs):
        jnt_pnt = jnt_list[i]
        jnt_pnt.setTranslation(vtx, OpenMaya.MSpace.kWorld)
    OpenMaya.MGlobal.setKeyframe(jnt_list)

