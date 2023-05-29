# -*- coding: utf-8 -*-
# @FileName :  fbx_importer.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/19 10:35
# @Software : PyCharm
# Description:
import os
import pymel.core as pm


class AdvAnimToolsUI:
    def __init__(self):
        self.fbxList = []
        self.savePath = None
        self.fbx_field = None
        self.path_field = None

    def create_ui(self):
        try:
            pm.deleteUI('advTool')
        except Exception as e:
            print(e)

        with pm.window('advTool', title='advAnimtools') as win:
            with pm.columnLayout(rowSpacing=5, adj=True):
                with pm.frameLayout(label='Import multiple FBX'):
                    with pm.columnLayout(adj=1):
                        pm.button(label="Load All fbx", c=self.load)
                    with pm.scrollLayout(w=200, h=150, bgc=(0.5, 0.5, 0.5)) as self.fbx_field:
                        pm.text('fbx Name:')
                    with pm.rowLayout(numberOfColumns=3,
                                      columnWidth3=(55, 140, 5),
                                      adjustableColumn=2,
                                      columnAlign=(1, 'right'),
                                      columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]
                                      ):
                        pm.text(label='Save Path:')
                        self.path_field = pm.textField("ImporterTextField")
                        pm.button(label='...', w=30, h=20, c=self.select_path)
                    with pm.columnLayout(adj=1):
                        pm.button(label="Import fbx And Save File !!!", c=self.import_and_save)

        pm.window(win, e=True, w=250, h=300)
        pm.showWindow(win)

    def load(self, *args):
        self.fbxList = pm.fileDialog2(fileFilter="*fbx", fileMode=4)

        if not self.fbxList:
            pm.PopupError('Nothing Selected')
            self.fbxList = []
            return

        for fbxPath in self.fbxList:
            fbx_name = os.path.basename(fbxPath)
            with self.fbx_field:
                pm.text(label=fbx_name)

    def select_path(self, *args):
        save_path = pm.fileDialog2(fileFilter='*folder', fileMode=2)
        if save_path:
            self.savePath = save_path[0]
            pm.textField(self.path_field, e=True, text=self.savePath)

    def import_and_save(self, *args):
        if not self.fbxList:
            pm.PopupError('Nothing To Import')
            return

        pm.currentUnit(time='ntsc')  # 30 fps

        fkik_attr = [
            "FKIKArm_L.FKIKBlend",
            "FKIKArm_R.FKIKBlend",
            "FKIKSpine_M.FKIKBlend",
            "FKIKLeg_R.FKIKBlend",
            "FKIKLeg_L.FKIKBlend"
        ]
        for a in fkik_attr:
            pm.setAttr(a, 0)

        for fbxPath in self.fbxList:
            pm.duplicate("NameMatcher:root")
            root_jnt = pm.PyNode("root")
            constarins = pm.ls(root_jnt, dag=True, type="constraint")  # 列出骨骼链的所有约束节点，注意参数dag
            pm.delete(constarins)

            pm.parentConstraint("root", "root_ctrl", mo=True)
            pm.parentConstraint("root", "Main", mo=True)
            pm.parentConstraint("pelvis", "RootX_M", mo=True)

            joint_sl = [
                "spine_01", "spine_02", "spine_03", "neck_01", "head", "clavicle_l", "upperarm_l", "lowerarm_l",
                "hand_l", "thumb_01_l", "thumb_02_l",
                "thumb_03_l", "index_01_l", "index_02_l", "index_03_l", "middle_01_l", "middle_02_l", "middle_03_l",
                "ring_01_l", "ring_02_l", "ring_03_l", "pinky_01_l",
                "pinky_02_l", "pinky_03_l", "clavicle_r", "upperarm_r", "lowerarm_r", "hand_r", "thumb_01_r",
                "thumb_02_r", "thumb_03_r", "index_01_r", "index_02_r",
                "index_03_r", "middle_01_r", "middle_02_r", "middle_03_r", "ring_01_r", "ring_02_r", "ring_03_r",
                "pinky_01_r", "pinky_02_r", "pinky_03_r", "thigh_l",
                "thigh_r", "calf_l", "calf_r", "foot_l", "foot_r", "ball_l", "ball_r"
            ]

            ctrl_sl = [
                "FKSpine1_M", "FKSpine2_M", "FKChest_M", "FKNeck_M", "FKHead_M", "FKScapula_L", "FKShoulder_L",
                "FKElbow_L", "FKWrist_L", "FKThumbFinger1_L",
                "FKThumbFinger2_L", "FKThumbFinger3_L", "FKIndexFinger1_L", "FKIndexFinger2_L", "FKIndexFinger3_L",
                "FKMiddleFinger1_L", "FKMiddleFinger2_L", "FKMiddleFinger3_L",
                "FKRingFinger1_L", "FKRingFinger2_L", "FKRingFinger3_L", "FKPinkyFinger1_L", "FKPinkyFinger2_L",
                "FKPinkyFinger3_L", "FKScapula_R", "FKShoulder_R", "FKElbow_R",
                "FKWrist_R", "FKThumbFinger1_R", "FKThumbFinger2_R", "FKThumbFinger3_R", "FKIndexFinger1_R",
                "FKIndexFinger2_R", "FKIndexFinger3_R", "FKMiddleFinger1_R",
                "FKMiddleFinger2_R", "FKMiddleFinger3_R", "FKRingFinger1_R", "FKRingFinger2_R", "FKRingFinger3_R",
                "FKPinkyFinger1_R", "FKPinkyFinger2_R", "FKPinkyFinger3_R",
                "FKHip_L", "FKHip_R", "FKKnee_L", "FKKnee_R", "FKAnkle_L", "FKAnkle_R", "IKToes_L", "IKToes_R"
            ]

            for i in range(len(joint_sl)):
                pm.parentConstraint(joint_sl[i], ctrl_sl[i], mo=True, skipTranslate=["x", "y", "z"])

            pm.importFile(fbxPath)

            first_frame = pm.findKeyframe('root', which="first")
            last_frame = pm.findKeyframe('root', which="last")
            pm.env.setMinTime(first_frame)
            pm.env.setMaxTime(last_frame)

            ctrl_bk = [
                'FKWeaponAS_R', 'FKRingFinger3_R', 'FKRingFinger2_R', 'FKRingFinger1_R', 'FKWrist_R', 'FKElbow_R',
                'FKShoulder_R', 'FKToes_R', 'FKAnkle_R', 'FKKnee_R', 'FKHip_R', 'FKToes_L', 'FKAnkle_L',
                'FKKnee_L', 'FKHip_L', 'RootX_M', 'AimEye_L', 'AimEye_R', 'AimEye_M', 'FKNeck_M', 'HipSwinger_M',
                'FKChest_M', 'FKSpine2_M', 'FKEye_R', 'FKJaw_M', 'FKHead_M', 'FKScapula_L', 'FKWeaponASB_R',
                'FKScapula_R', 'FKEye_L', 'FKThumbFinger2_R', 'FKThumbFinger1_R', 'FKMiddleFinger3_R',
                'FKMiddleFinger2_R', 'FKMiddleFinger1_R', 'FKThumbFinger1_L', 'FKMiddleFinger3_L', 'FKMiddleFinger2_L',
                'FKMiddleFinger1_L', 'FKIndexFinger2_L', 'FKIndexFinger1_L', 'FKThumbFinger3_L', 'FKThumbFinger2_L',
                'FKIndexFinger3_R', 'FKIndexFinger2_R', 'FKIndexFinger1_R', 'FKThumbFinger3_R', 'FKPinkyFinger3_R',
                'FKPinkyFinger2_R', 'FKPinkyFinger1_R', 'FKCup_R', 'MainExtra2', 'FKSpine1_M', 'FKRoot_M', 'root_ctrl',
                'Main', 'MainExtra1', 'FKPinkyFinger2_L', 'FKPinkyFinger1_L', 'FKCup_L', 'FKIndexFinger3_L',
                'FKRingFinger3_L',
                'FKRingFinger2_L', 'FKRingFinger1_L', 'FKPinkyFinger3_L', 'Fingers_L', 'Fingers_R', 'FKWrist_L',
                'FKElbow_L', 'FKShoulder_L', 'PoleLeg_R', 'IKToes_R', 'RollToes_R', 'RollToesEnd_R', 'RollHeel_R',
                'IKLeg_L',
                'PoleLeg_L', 'IKToes_L', 'RollToes_L', 'RollToesEnd_L', 'RollHeel_L', 'IKLeg_R', 'FKWeaponAS_L'
            ]
            pm.bakeResults(ctrl_bk, simulation=True, time=(first_frame, last_frame), sampleBy=1, oversamplingRate=1,
                           disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False,
                           removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False,
                           bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=True)
            pm.filterCurve(ctrl_bk)
            pm.delete('root')
            print("Done")

            if self.savePath:
                short_name = os.path.splitext(os.path.basename(fbxPath))[0]
                file_path = os.path.join(self.savePath, short_name + ".mb")
                print(file_path)
                pm.saveAs(file_path, force=True)

        confirm = pm.confirmDialog(title='Finish', message="Done!", button=['OK', 'Open Folder'])
        if confirm == 'Open Folder' and self.savePath:
            os.startfile(self.savePath)


if __name__ == '__main__':
    advAnimToolsUI = AdvAnimToolsUI()
    advAnimToolsUI.create_ui()
