# -*- coding: utf-8 -*-
# @FileName :  pose_tools.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/25 16:13
# @Software : PyCharm
# Description:
import pymel.core as pm


class PoseToolsUI:
    def __init__(self):
        self.attr = []
        self.attrVal = []
        self.data = {}
        self.template = pm.uiTemplate('cpTemplate', force=True)
        self.template.define(pm.button, width=200, height=30, align='right')
        self.template.define(pm.frameLayout, borderVisible=True, labelVisible=False)
        self.createUI()

    def createUI(self):
        if pm.window('cpWindow', exists=1):
            pm.deleteUI('cpWindow', window=True)
        with pm.window('cpWindow', menuBarVisible=True, title='CopyNPastPose') as win:
            with self.template:
                with pm.columnLayout(rowSpacing=5, adj=1):
                    with pm.frameLayout():
                        with pm.columnLayout(adj=1):
                            pm.button(label='Copy Pose', c=self.copyPose)
                            pm.button(label='Paste Pose', c=self.pastePose)
                            pm.button(label='Paste Mirror Pose', c=self.pasteMirPose)
                            pm.button(label="Mirror Animation", c=self.mirror_anim)
        pm.showWindow(win)

    def copyPose(self, *args):
        sel_obj = pm.selected()
        attr_list = [i.listAnimatable() for i in sel_obj]

        for i in attr_list:
            for y in i:
                x = str(y)
                self.attr.append(x)

        self.attrVal = [pm.getAttr(s) for s in self.attr]

        zip_list = zip(self.attr, self.attrVal)
        self.data = dict(zip_list)

    def pastePose(self, *args):
        for key, value in self.data.items():
            pm.setAttr(key, value)

    def pasteMirPose(self, *args):
        mir_list = []
        for a in self.attr:
            if '_L' in a:
                mir = a.replace('_L', '_R')
            elif '_R' in a:
                mir = a.replace('_R', '_L')
            else:
                mir = a
            mir_list.append(mir)

        mir_zip_list = zip(mir_list, self.attrVal)
        mir_data = dict(mir_zip_list)

        for key, value in mir_data.items():
            if ('IK' in key or 'Pole' in key) and ('translateX' in key or 'rotateY' in key or 'rotateZ' in key):
                pm.setAttr(key, value * -1)
            elif ('RootX_M' in key) and ('translateX' in key or 'rotateY' in key or 'rotateZ' in key):
                pm.setAttr(key, value * -1)
            elif ('FKRoot' in key or 'Spine' in key or 'Chest' in key or 'Neck' in key or 'Head' in key) and (
                    'rotateX' in key or 'rotateY' in key):
                pm.setAttr(key, value * -1)
            else:
                pm.setAttr(key, value)

    def mirror_anim(self, *args):
        first_frame = pm.env.getMinTime()
        last_frame = pm.env.getMaxTime()
        for frame in range(int(first_frame), int(last_frame)+1):
            pm.currentTime(frame)
            self.copyPose()
            self.pasteMirPose()


# Create an instance of the CopyNPastePoseUI class to run the script
ui = PoseToolsUI()
