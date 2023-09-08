import maya.cmds as cmds


class SkelToBones:
    """
    为骨骼创建盒体代理模型
    """

    def __init__(self):
        print("Skeleton to Geometry Instance.")

    def create_poly_sphere(self, name="poly_sphere"):
        """
        Creates a polygonal sphere with the given name.

        Args:
            name (str, optional): The name of the polygonal sphere. Defaults to "poly_sphere".

        Returns:
            str: The name of the created polygonal sphere.
        """
        geometry = cmds.polySphere(
            name=name, r=1, sx=20, sy=20, ax=(-1, 0, 0), cuv=2, ch=False
        )[0]

        return geometry

    def create_poly_cube(self, name="poly_cube"):
        """
        Creates a polygonal cube with the given name.

        Args:
            name (str, optional): The name of the cube. Defaults to "poly_cube".

        Returns:
            str: The name of the created cube.

        Raises:
            None
        """
        geometry = cmds.polyCube(
            name=name, w=1, h=1, d=1, sx=1, sy=1, sz=1, ax=(0, 1, 0), cuv=4, ch=False
        )[0]

        if not cmds.objExists("MI_red_X"):
            x_shader = self.create_lambert_shader("MI_red_X", (1, 0, 0))
        else:
            x_shader = "MI_red_X"
        if not cmds.objExists("MI_green_Y"):
            y_shader = self.create_lambert_shader("MI_green_Y", (0, 1, 0))
        else:
            y_shader = "MI_green_Y"
        if not cmds.objExists("MI_blue_Z"):
            z_shader = self.create_lambert_shader("MI_blue_Z", (0, 0, 1))
        else:
            z_shader = "MI_blue_Z"

        self.assing_shader_to_geometry(x_shader, geometry + ".f[4]")
        self.assing_shader_to_geometry(x_shader, geometry + ".f[5]")
        self.assing_shader_to_geometry(y_shader, geometry + ".f[1]")
        self.assing_shader_to_geometry(y_shader, geometry + ".f[3]")
        self.assing_shader_to_geometry(z_shader, geometry + ".f[2]")
        self.assing_shader_to_geometry(z_shader, geometry + ".f[0]")

        return geometry

    def create_poly_pyramid(self, name="poly_pyramid"):
        """
        Create a poly pyramid with the given name.

        Args:
            name (str, optional): The name of the poly pyramid. Defaults to "poly_pyramid".

        Returns:
            str: The name of the created geometry.
        """
        geometry = cmds.polyPyramid(
            name=name, w=1, ns=4, sh=1, sc=0, ax=(0, 1, 0), cuv=3, ch=False
        )[0]
        cmds.setAttr(geometry + ".translateY", 0.354)
        cmds.select(geometry, r=True)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)

        return geometry

    def create_lambert_shader(self, name, color=(1, 0, 0)):
        """
        Creates a Lambert shader with the given name and color.

        Args:
            name (str): The name of the shader.
            color (tuple, optional): The RGB color of the shader. Defaults to (1, 0, 0).

        Returns:
            tuple: A tuple containing the shader and shading group nodes.
        """
        shader = cmds.shadingNode("lambert", asShader=True, name=name)
        shading_group = cmds.sets(
            name=name + "SG",
            empty=True,
            renderable=True,
            noSurfaceShader=False,
        )
        cmds.connectAttr(shader + ".outColor", shading_group + ".surfaceShader", f=True)
        cmds.setAttr(
            shader + ".color",
            color[0],
            color[1],
            color[2],
            type="double3",
        )
        return shader, shading_group

    def assing_shader_to_geometry(self, shader, geometry):
        """
        Assigns a shader to a geometry.

        Parameters:
            shader (str): The name of the shader to be assigned.
            geometry (str): The name of the geometry to assign the shader to.

        Returns:
            None
        """
        shading_engine = cmds.listConnections(shader, type="shadingEngine")[0]
        cmds.sets(geometry, forceElement=shading_engine)

    def compute(
        self,
        skel_root="root",
        shape="boint",
        pyramid_scale_multiplier=1,
        sphere_scale_multiplier=1,
        auto_skin=True,
    ):
        """
        Computes the new geometries based on the given parameters.

        Args:
            skel_root (str, optional): The name of the root joint. Defaults to "root".
            shape (str, optional): The shape of the geometry to create. Can be "boint" or "cube". Defaults to "boint".
            pyramid_scale_multiplier (float, optional): The scale multiplier for the pyramid shape. Defaults to 1.
            sphere_scale_multiplier (float, optional): The scale multiplier for the sphere shape. Defaults to 1.
            auto_skin (bool, optional): Whether or not to automatically skin the geometries. Defaults to True.

        Returns:
            None
        """
        new_geometries = []
        cmds.select(skel_root, hierarchy=True, r=True)
        bones = cmds.ls(sl=True, type="joint")
        if shape == "boint":
            for bone in bones:
                if bone != skel_root:
                    bone_radius = cmds.getAttr(bone + ".radius")
                    bone_sphere = self.create_poly_sphere(bone + "Sphere_geo")
                    new_geometries.append(bone_sphere)
                    cmds.delete(cmds.parentConstraint(bone, bone_sphere, mo=False))
                    bone_parent = cmds.listRelatives(bone, p=True)[0]
                    bone_pyramid = self.create_poly_pyramid(bone + "Pyramid_geo")
                    new_geometries.append(bone_pyramid)
                    cmds.delete(
                        cmds.parentConstraint(bone_parent, bone_pyramid, mo=False)
                    )
                    cmds.delete(
                        cmds.aimConstraint(
                            bone, bone_pyramid, aimVector=(0, 1, 0), mo=False
                        )
                    )
                    cmds.setAttr(bone_pyramid + ".sx", pyramid_scale_multiplier)
                    cmds.setAttr(bone_pyramid + ".sz", pyramid_scale_multiplier)
                    cmds.setAttr(
                        bone_sphere + ".sx", bone_radius / 2 * sphere_scale_multiplier
                    )
                    cmds.setAttr(
                        bone_sphere + ".sy", bone_radius / 2 * sphere_scale_multiplier
                    )
                    cmds.setAttr(
                        bone_sphere + ".sz", bone_radius / 2 * sphere_scale_multiplier
                    )
                    cmds.select(bone_pyramid + ".vtx[4]", r=True)
                    cluster_handle = cmds.cluster()[1]
                    cmds.delete(cmds.parentConstraint(bone, cluster_handle))
                    cmds.delete(bone_pyramid, constructionHistory=True)

                    if auto_skin:
                        pyramid_skinCluster = cmds.skinCluster(
                            [bone, bone_parent],
                            bone_pyramid,
                            tsb=True,
                            name=bone_pyramid + "_skinCluster",
                            mi=1,
                        )[0]
                        cmds.skinCluster(
                            [bone],
                            bone_sphere,
                            tsb=True,
                            name=bone_sphere + "_skinCluster",
                            mi=1,
                        )
                        cmds.skinPercent(
                            pyramid_skinCluster,
                            bone_pyramid + ".vtx[4]",
                            tv=[(bone, 1)],
                        )

                        cmds.skinPercent(
                            pyramid_skinCluster,
                            bone_pyramid + ".vtx[0:3]",
                            tv=[(bone_parent, 1)],
                        )
            bone_geometry = cmds.polyUniteSkinned(
                new_geometries, ch=False, mergeUVSets=True
            )[0]
            bone_geometry = cmds.rename(bone_geometry, skel_root + "_geo")
            if not cmds.objExists("MI_boint"):
                boint_shader = self.create_lambert_shader("MI_boint", (0.3, 0.15, 0.3))
            else:
                boint_shader = "MI_boint"
            self.assing_shader_to_geometry(boint_shader, bone_geometry)

        if shape == "cube":
            for bone in bones:
                if bone != skel_root:
                    bone_childs = cmds.listRelatives(bone, children=True)
                    bone_parent = cmds.listRelatives(bone, p=True)[0]
                    bone_cube = self.create_poly_cube(bone_parent + "Cube_geo")
                    new_geometries.append(bone_cube)
                    cmds.setAttr(bone_cube + ".sz", sphere_scale_multiplier)
                    cmds.setAttr(bone_cube + ".sy", sphere_scale_multiplier)

                    cmds.delete(cmds.parentConstraint(bone_parent, bone_cube, mo=False))
                    cmds.delete(cmds.aimConstraint(bone, bone_cube, mo=False))
                    cmds.select(bone_cube + ".f[5]", r=True)
                    cluster_handle = cmds.cluster()[1]
                    cmds.delete(cmds.pointConstraint(bone_parent, cluster_handle))
                    cmds.delete(bone_cube, constructionHistory=True)
                    cmds.select(bone_cube + ".f[4]", r=True)
                    cluster_handle = cmds.cluster()[1]
                    cmds.delete(cmds.pointConstraint(bone, cluster_handle))
                    cmds.delete(bone_cube, constructionHistory=True)
                    if bone_childs is None:
                        bone_cube_second = self.create_poly_cube(bone + "Cube_geo")
                        cmds.delete(
                            cmds.parentConstraint(bone, bone_cube_second, mo=False)
                        )
                        new_geometries.append(bone_cube_second)
                        cmds.skinCluster(
                            [bone],
                            bone_cube_second,
                            tsb=True,
                            name=bone_cube_second + "_skinCluster",
                            mi=1,
                        )[0]

                    if auto_skin:
                        cmds.skinCluster(
                            [bone_parent],
                            bone_cube,
                            tsb=True,
                            name=bone_cube + "_skinCluster",
                            mi=1,
                        )[0]
            bone_geometry = cmds.polyUniteSkinned(
                new_geometries, ch=False, mergeUVSets=True
            )[0]
            cmds.rename(bone_geometry, skel_root + "_geo")

    def ui(self, *args):
        """
        Initializes the user interface for the Skeleton to Geometry Alpha v.01 tool.

        Args:
            *args: Variable length argument list.

        Returns:
            None
        """
        window = "Skeleton to Geometry Alpha v.01"
        title = "Skeleton to Geometry Alpha v.01"
        size = (400, 600)

        # close old window is open
        if cmds.window(window, exists=True):
            cmds.deleteUI(window, window=True)

        # create new window
        window = cmds.window(window, title=title, widthHeight=size)

        cmds.columnLayout(adjustableColumn=True)

        cmds.text(title)
        cmds.separator(height=20)

        self.skeleton_root = cmds.textFieldGrp(label="Skeleton Root:")
        self.geometry_type = cmds.textFieldGrp(label="Geometry Type:")
        self.scale_multiplier = cmds.textFieldGrp(label="Scale:")

        cmds.text("Geometry type options are:")
        cmds.text("1) boint for Bone + Joint mesh")
        cmds.text("2) cube for cube based geometry")

        cmds.button(label="Do It!", command=self.do_it)
        cmds.showWindow()

    def do_it(self, *args):
        """
        Generate the function comment for the given function body in a markdown code block
        with the correct language syntax.

        :param args: The arguments passed to the function.
        :type args: tuple
        """
        skeleton_root_value = cmds.textFieldGrp(self.skeleton_root, q=True, text=True)
        geometry_type_value = cmds.textFieldGrp(self.geometry_type, q=True, text=True)
        scale_value = int(cmds.textFieldGrp(self.scale_multiplier, q=True, text=True))

        self.compute(
            skeleton_root_value, geometry_type_value, scale_value, scale_value, True
        )


if __name__ == "__main__":
    my_s2g = SkelToBones()
    my_s2g.ui()
