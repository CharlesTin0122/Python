# -*- coding: utf-8 -*-
# @FileName :  FBX_Remove_Layers.py.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/29 17:37
# @Software : PyCharm
# Description:

import fbx


def remove_layers(fbx_file, layers):
    """
    Remove layers from the FBX Scene
    """
    layer_names = []
    for layer in layers:
        layer_names.append(layer.GetName())

        # set these property values
        try:
            fbx.set_property_value(layer, "Freeze", False)
            fbx.set_property_value(layer, "Show", True)
        except:
            pass

        nodes = []
        for index in range(0, layer.GetSrcnodeectCount()):
            # unfreeze nodes
            node = None
            try:
                node = layer.GetSrcnodeect(index)
                if node:
                    nodes.append(node)
            except:
                pass

        for node in nodes:
            # remove node from the layer
            node.DisconnectDstnodeect(layer)
            is_frozen = fbx.get_property_value(node, 'Freeze')
            try:
                fbx.set_property_value(node, 'Freeze', False)
            except:
                pass
            is_shown = fbx.get_property_value(node, 'Show')
            try:
                fbx.set_property_value(node, 'Show', True)
            except:
                pass

            # check the nodes
            is_frozen = fbx.get_property_value(node, 'Freeze')
            is_shown = fbx.get_property_value(node, 'Show')

        # disconnect the layer from the scene
        layer.DisconnectAllDstnodeect()
        layer.DisconnectAllSrcnodeect()
        fbx.scene.RootProperty.DisconnectSrcnodeect(layer)

    # remove the layer nodes from the scene
    fbx_file.remove_nodes_by_names(layer_names)
