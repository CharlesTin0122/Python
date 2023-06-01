# -*- coding: utf-8 -*-
# @FileName :  FBX_Character_Cleanup.py.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/29 17:31
# @Software : PyCharm
# Description:
import fbx
import fbx_scene


def clean_character_scene(fbx_filename):
    """
    Clean up character FBX file
    """
    # Open the FBX scene and get the scene nodes
    fbx_file = fbx_scene.FbxClass(fbx_filename)
    if not fbx_file:
        return False

    # Remove invalid nodes noted by properties assigned in the DCC application
    all_nodes = fbx_file.get_scene_nodes()
    remove_names = []
    for node in all_nodes:
        export_property = fbx_file.get_property(node, 'no_export')
        if export_property:
            property_value = fbx_file.get_property_value(node, 'no_export')
            if property_value:
                node_name = node.GetName()
                # Need to disconnect before deleting/removing
                fbx_file.scene.DisconnectSrcObject(node)
                remove_names.append(node_name)

    # Remove the nodes from the scene by name
    fbx_file.remove_nodes_by_names(remove_names)

    # Remove FbxContainers
    nodes = fbx_file.get_class_nodes(fbx.FbxObject.ClassId)
    if nodes:
        for node in nodes:
            if node.GetClassId().GetName() == 'FbxContainer':
                # Disconnect the layer from the scene
                node.DisconnectAllDstObject()
                node.DisconnectAllSrcObject()
                fbx_file.scene.RootProperty.DisconnectSrcObject(node)

    # Save the modified FBX scene
    fbx_file.save()

    return True
