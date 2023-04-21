import pymel.core as pm


def resetBindPose(jnts, selected_only=False):
    """
	Resets the bind pose as if the skin was bound to the skeleton as it exists now it world space.

	:param jnts: `List` of joints to be reset. Use in conjunction with selected flag to get hierarchy.

	:param selected_only: By default will include all children of given jnts unless this is set to True.

	:return: None
	"""
    jnts = makePyNodeList(jnts)

    jnts_to_reset = set()
    if selected_only:
        jnts_to_reset |= set(jnts)
    else:
        for jnt in jnts:
            children = jnt.getChildren(ad=True, type='joint')
            jnts_to_reset |= set(children)

    pm.dagPose(jnts_to_reset, bindPose=True, reset=True)

    for jnt in jnts_to_reset:
        inv_world_mtx = jnt.worldInverseMatrix[0].get()

        skin_outputs = jnt.worldMatrix[0].outputs(p=True, type='skinCluster')
        for skin in skin_outputs:
            joint_index = skin.index()

            pre_mtx_attr = skin.node().attr('bindPreMatrix')

            jnt_pre_mtx = pre_mtx_attr.elementByLogicalIndex(joint_index)
            jnt_pre_mtx.set(inv_world_mtx)
