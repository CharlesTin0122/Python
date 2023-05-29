# -*- coding: utf-8 -*-
# @FileName :  fbx_exporter.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/19 9:38
# @Software : PyCharm
# Description:
import os

import pymel.core as pm


class FbxExporterUI(object):

    def __init__(self):
        self.export_path_field = None
        self.fileList = []
        self.objList = []
        self.exportPath = None
        self.window = None
        self.slyFile = None
        self.slyOBJ = None

    def show(self):
        try:
            pm.deleteUI('fbxExport')
        except Exception as exc:
            print(exc)

        self.window = pm.window('fbxExport', title='FBX Exporter')
        with pm.columnLayout(rowSpacing=5, adj=True):
            with pm.frameLayout(label='Export multiple files'):
                with pm.columnLayout(adj=1):
                    pm.button(label='Load All Export Files', c=self.load_files)
                with pm.scrollLayout(w=200, h=150, bgc=(0.5, 0.5, 0.5)) as self.slyFile:
                    pm.text('File Name:')
                with pm.columnLayout(adj=1):
                    pm.button(label='Load Objects To Export', c=self.load_objects)
                with pm.scrollLayout(w=200, h=150, bgc=(0.5, 0.5, 0.5)) as self.slyOBJ:
                    pm.text('OBJ Name:')
                with pm.rowLayout(numberOfColumns=3,
                                  columnWidth3=(55, 140, 5),
                                  adjustableColumn=2,
                                  columnAlign=(1, 'right'),
                                  columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)]
                                  ):
                    pm.text(label='Export Path:', w=65)
                    self.export_path_field = pm.textField("ExporterTextField")
                    pm.button(label='...', w=30, h=20, c=self.select_export_path)
                with pm.columnLayout(adj=1):
                    pm.button(label='Export All !!!', c=self.export_all)
        self.window.show()

    def load_files(self, *args):
        self.fileList = pm.fileDialog2(fileFilter='*mb', fileMode=4)
        if not self.fileList:
            pm.warning('No files selected for export.')
            return
        with self.slyFile:
            for file in self.fileList:
                pm.text(label=os.path.basename(file))

    def load_objects(self, *args):
        self.objList = pm.selected()
        if not self.objList:
            pm.warning('No objects selected for export.')
            return
        with self.slyOBJ:
            for obj in self.objList:
                pm.text(label=obj)

    def select_export_path(self, *args):
        export_path = pm.fileDialog2(fileFilter='*folder', fileMode=2)
        if export_path:
            self.exportPath = export_path[0]
            pm.textField(self.export_path_field, e=True, text=self.exportPath)

    def export_all(self, *args):
        if not self.fileList:
            pm.warning('No files selected for export.')
            return
        if not self.objList:
            pm.warning('No objects selected for export.')
            return
        if not self.exportPath:
            pm.warning('No export path selected.')
            return
        for f in self.fileList:
            file_name = os.path.basename(f)
            bace_name = os.path.splitext(file_name)
            exp_name = str(bace_name[0]) + '.fbx'
            pm.openFile(f, force=True)
            pm.select(self.objList)
            pm.bakeResults(t=(pm.env.getMaxTime(), pm.env.getMinTime()), bol=True)
            pm.select(self.objList)
            pm.exportSelected(
                os.path.join(self.exportPath, exp_name),
                force=True, type='FBX export',
                constructionHistory=False,
                constraints=False,
                expressions=False
            )
            pm.delete('BakeResultsContainer')
        pm.informBox(title='Export Complete', message='All selected objects have been exported successfully.')


if __name__ == '__main__':
    ui = FbxExporterUI()
    ui.show()
