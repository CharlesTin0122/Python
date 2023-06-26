# -*- coding: utf-8 -*-
# @FileName :  batch_mayafile_excute.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/1 14:58
# @Software : PyCharm
# Description:
import os
import pymel.core as pm


class BatchMayaFile:
    def __init__(self):
        self.file_list = []
        self.savePath = None
        self.file_field = None
        self.path_field = None

    def create_ui(self):
        try:
            pm.deleteUI('Batch Tool')
        except Exception as e:
            print(e)

        with pm.window('Batch Tool', title='Maya Batch Tool') as win:
            with pm.columnLayout(rowSpacing=5, adj=True):
                with pm.frameLayout(label='Load Maya File'):
                    with pm.columnLayout(adj=1):
                        pm.button(label="Load ALL Maya File", c=self.load)
                    with pm.scrollLayout(w=200, h=150, bgc=(0.5, 0.5, 0.5)) as self.file_field:
                        pm.text('File Name:')
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
                        pm.button(label="Batch !!!", c=self.doit)

        pm.window(win, e=True, w=250, h=300)
        pm.showWindow(win)

    def load(self, *args):
        self.file_list = pm.fileDialog2(fileFilter='All Files (*.*)', fileMode=4)

        if not self.file_list:
            pm.PopupError('Nothing Selected')
            self.file_list = []
            return

        for file_path in self.file_list:
            file_name = os.path.basename(file_path)
            with self.file_field:
                pm.text(label=file_name)

    def select_path(self, *args):
        save_path = pm.fileDialog2(fileFilter='*folder', fileMode=2)
        if save_path:
            self.savePath = save_path[0]
            pm.textField(self.path_field, e=True, text=self.savePath)

    def doit(self, *args):
        if not self.file_list:
            pm.PopupError('Nothing To Batch')
            return

        """--------------------------之下为批量执行代码-------------------------------------"""

        pm.currentUnit(time='ntsc')  # 30 fps

        for file in self.file_list:
            pm.openFile(file, force=True)
            weapon_jnt = pm.PyNode("weapon_R")

            translate_cv = weapon_jnt.listConnections(type="animCurveTL")
            rotate_cv = weapon_jnt.listConnections(type="animCurveTA")
            scale_cv = weapon_jnt.listConnections(type="animCurveTU")
            try:
                pm.delete(translate_cv, rotate_cv, scale_cv)
            except Exception as e:
                print(e)

            weapon_jnt.setTranslation([8.8, 3.301, 0.259])
            weapon_jnt.setRotation([-98.928, 14.932, -6.117])
            pm.setKeyframe(weapon_jnt)

            if self.savePath:
                short_name = os.path.splitext(os.path.basename(file))[0]
                file_path = os.path.join(self.savePath, short_name + ".fbx")
                print(file_path)
                pm.exportAll(file_path, force=True)
        """----------------------------------之上为批量执行代码---------------------------------------"""

        confirm = pm.confirmDialog(title='Finish', message="Done!", button=['OK', 'Open Folder'])
        if confirm == 'Open Folder' and self.savePath:
            os.startfile(self.savePath)


if __name__ == '__main__':
    batchtool = BatchMayaFile()
    batchtool.create_ui()
