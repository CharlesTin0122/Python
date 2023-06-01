# -*- coding: utf-8 -*-
"""
This is a helper FBX class useful in accessing and modifying the FBX Scene
Documentation for the FBX SDK
http://help.autodesk.com/view/FBX/2015/ENU/?guid=__cpp_ref_index_html
Examples:
# instantiate the class, as seen below with a path to an FBX file
fbx_file = FBX_Class(r'c:\\my_path\\character.fbx')
#get all the scene nodes
all_fbx_nodes = fbx_file.file.scene_nodes()
# remove namespaces from all the nodes
fbx_file.remove_namespace()
# get the display layer objects
display_layer_nodes = fbx_file.get_type_nodes( u'DisplayLayer' )
geometry_nodes = fbx_file.get_class_nodes( fbx_file.FbxGeometry.ClassId )
# save the file that was given
fbx_file.save_scene()
# cleanly close the fbx scene.
# YOU SHOULD ALWAYS CLOSE WHEN FINISHED WITH THE FILE
fbx_file.close()
"""

import FbxCommon
import fbx


class FbxClass(object):

    def __init__(self, filename):
        """
         构造方法用于初始化FbxClass对象。它接受一个文件名作为参数，初始化FBX SDK管理器和场景，并加载指定文件名的FBX文件
        """
        self.filename = filename
        self.scene = None
        self.sdk_manager = None
        self.sdk_manager, self.scene = FbxCommon.InitializeSdkObjects()
        FbxCommon.LoadScene(self.sdk_manager, self.scene, filename)

        self.root_node = self.scene.GetRootNode()
        self.scene_nodes = self.get_scene_nodes()

    def close(self):
        """
        这个方法用于安全地关闭FBX场景。它销毁FBX SDK创建的对象
        """
        # destroy objects created by the sdk
        self.sdk_manager.Destroy()

    def __get_scene_nodes_recursive(self, node):
        """
        Rescursive method to get all scene nodes
        this should be private, called by get_scene_nodes()
        这是一个私有递归方法，由get_scene_nodes()在内部使用，用于获取FBX文件中的所有场景节点。
        """
        self.scene_nodes.append(node)
        for i in range(node.GetChildCount()):
            self.__get_scene_nodes_recursive(node.GetChild(i))

    @staticmethod
    def __cast_property_type(fbx_property):
        """
        Cast a property to type to properly get the value
        这是一个静态方法，用于将FBX属性强制转换为适当的类型，以便获取其值。它支持各种属性类型，例如布尔型、双精度浮点型、字符串等。
        """
        casted_property = None

        unsupported_types = [fbx.eFbxUndefined, fbx.eFbxChar, fbx.eFbxUChar, fbx.eFbxShort, fbx.eFbxUShort,
                             fbx.eFbxUInt,
                             fbx.eFbxLongLong, fbx.eFbxHalfFloat, fbx.eFbxDouble4x4, fbx.eFbxEnum, fbx.eFbxTime,
                             fbx.eFbxReference, fbx.eFbxBlob, fbx.eFbxDistance, fbx.eFbxDateTime, fbx.eFbxTypeCount]

        # property is not supported or mapped yet
        property_type = fbx_property.GetPropertyDataType().GetType()
        if property_type in unsupported_types:
            return None

        if property_type == fbx.eFbxBool:
            casted_property = fbx.FbxPropertyBool1(fbx_property)
        elif property_type == fbx.eFbxDouble:
            casted_property = fbx.FbxPropertyDouble1(fbx_property)
        elif property_type == fbx.eFbxDouble2:
            casted_property = fbx.FbxPropertyDouble2(fbx_property)
        elif property_type == fbx.eFbxDouble3:
            casted_property = fbx.FbxPropertyDouble3(fbx_property)
        elif property_type == fbx.eFbxDouble4:
            casted_property = fbx.FbxPropertyDouble4(fbx_property)
        elif property_type == fbx.eFbxInt:
            casted_property = fbx.FbxPropertyInteger1(fbx_property)
        elif property_type == fbx.eFbxFloat:
            casted_property = fbx.FbxPropertyFloat1(fbx_property)
        elif property_type == fbx.eFbxString:
            casted_property = fbx.FbxPropertyString(fbx_property)
        else:
            raise ValueError(
                'Unknown property type: {0} {1}'.format(property.GetPropertyDataType().GetName(), property_type))

        return casted_property

    def get_scene_nodes(self):
        """
        Get all nodes in the fbx scene
        获取FBX场景中的所有节点
        """
        self.scene_nodes = []
        for i in range(self.root_node.GetChildCount()):
            self.__get_scene_nodes_recursive(self.root_node.GetChild(i))
        return self.scene_nodes

    def get_type_nodes(self, type):
        """
        Get nodes from the scene with the given type
        display_layer_nodes = fbx_file.get_type_nodes( u'DisplayLayer' )
        获取具有给定类型的节点
        """
        nodes = []
        num_objects = self.scene.RootProperty.GetSrcObjectCount()
        for i in range(0, num_objects):
            node = self.scene.RootProperty.GetSrcObject(i)
            if node:
                if node.GetTypeName() == type:
                    nodes.append(node)
        return nodes

    def get_class_nodes(self, class_id):
        """
        Get nodes in the scene with the given classid
        geometry_nodes = fbx_file.get_class_nodes( fbx.FbxGeometry.ClassId )
        获取具有给定Class ID的节点
        """
        nodes = []
        num_nodes = self.scene.RootProperty.GetSrcObjectCount(fbx.FbxCriteria.ObjectType(class_id))
        for index in range(0, num_nodes):
            node = self.scene.RootProperty.GetSrcObject(fbx.FbxCriteria.ObjectType(class_id), index)
            if node:
                nodes.append(node)
        return nodes

    @staticmethod
    def get_property(node, property_string):
        """
        Gets a property from a Fbx node
        export_property = fbx_file.get_property(node, 'no_export')
        从FBX节点获取属性
        """
        fbx_property = node.FindProperty(property_string)
        return fbx_property

    def get_property_value(self, node, property_string):
        """
        Gets the property value from an Fbx node
        property_value = fbx_file.get_property_value(node, 'no_export')
        获取FBX节点的属性值
        """
        fbx_property = node.FindProperty(property_string)
        if fbx_property.IsValid():
            # cast to correct property type so you can get
            casted_property = self.__cast_property_type(fbx_property)
            if casted_property:
                return casted_property.Get()
        return None

    def get_node_by_name(self, name):
        """
        Get the fbx node by name
        根据名称获取FBX节点
        """
        self.get_scene_nodes()
        # right now this is only getting the first one found
        node = [node for node in self.scene_nodes if node.GetName() == name]
        if node:
            return node[0]
        return None

    def remove_namespace(self):
        """
        Remove all namespaces from all nodes
        This is not an ideal method but
        从所有节点中移除命名空间
        """
        self.get_scene_nodes()
        for node in self.scene_nodes:
            orig_name = node.GetName()
            split_by_colon = orig_name.split(':')
            if len(split_by_colon) > 1:
                new_name = split_by_colon[-1:][0]
                node.SetName(new_name)
        return True

    def remove_node_property(self, node, property_string):
        """
        Remove a property from a Fbx node
        remove_property = fbx_file.remove_property(node, 'UDP3DSMAX')
        从FBX节点中移除属性
        """
        node_property = self.get_property(node, property_string)
        if node_property.IsValid():
            node_property.DestroyRecursively()
            return True
        return False

    def remove_nodes_by_names(self, names):
        """
        Remove nodes from the fbx file from a list of name
        names = ['object1','shape2','joint3']
        remove_nodes = fbx_file.remove_nodes_by_names(names)
        从FBX文件中移除指定名称的节点
        """

        if names is None or len(names) == 0:
            return True

        self.get_scene_nodes()
        remove_nodes = [node for node in self.scene_nodes if node.GetName() in names]
        for node in remove_nodes:
            disconnect_node = self.scene.DisconnectSrcObject(node)
            remove_node = self.scene.RemoveNode(node)
        self.get_scene_nodes()
        return True

    def save(self, filename=None):
        """
        Save the current fbx scene as the incoming filename .fbx
        将当前的FBX场景保存为指定的文件名
        """
        # save as a different filename
        if filename is not None:
            FbxCommon.SaveScene(self.sdk_manager, self.scene, filename)
        else:
            FbxCommon.SaveScene(self.sdk_manager, self.scene, self.filename)
        self.close()
        return True


if __name__ == "__main__":
    # instantiate the class, as seen below with a path to an FBX file
    fbx_file = FbxClass(r"c:\my_path\character.fbx")
    # get all  the scene nodes
    all_fbx_nodes = fbx_file.get_scene_nodes()
    # get node by name
    node = fbx_file.get_node_by_name("head")
    # remove nodes by names
    remove_node = fbx_file.remove_nodes_by_names("hair_a_01")
    # remove namespaces from all  the nodes
    fbx_file.remove_namespace()
    # get the display layer objects
    display_layer_nodes = fbx_file.get_type_nodes("DisplayLayer")
    # node_property = fbx_file.get_property(node1, 'no_export')
    # node_property_value = fbx_file.get_property_value(node2, 'no_export')
    # remove_property = fbx_file.remove_node_property(node3, 'no_anim_export')
    geometry_nodes = fbx_file.get_class_nodes(fbx.FbxGeometry.ClassId)
    # save the file that was given
    fbx_file.save()
    save_file = fbx_file.save(filename=r"d:\temp.fbx")
    # cleanly close the fbx scene.
    # YOU SHOULD ALWAYS CLOSE WHEN FINISHED WITH THE FILE
    fbx_file.close()
