# -*- coding: utf-8 -*-
# @FileName :  Run_Maya_in_Batch_Mode.py.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/4/21 11:41
# @Software : PyCharm
# Description:
import os
import sys
import maya.cmds as cmds
import maya.standalone

MAYA_LOCATION = r"C:\Program Files\Autodesk\Maya2023"
PYTHON_LOCATION = MAYA_LOCATION + "/Python/Lib/site-packages"

os.environ["MAYA_LOCATION"] = MAYA_LOCATION
os.environ["PYTHONPATH"] = PYTHON_LOCATION

sys.path.append(MAYA_LOCATION)
sys.path.append(PYTHON_LOCATION)
sys.path.append(MAYA_LOCATION + "/bin")
sys.path.append(MAYA_LOCATION + "/lib")
sys.path.append(MAYA_LOCATION + "/Python")
sys.path.append(MAYA_LOCATION + "/Python/DLLs")
sys.path.append(MAYA_LOCATION + "/Python/Lib")
sys.path.append(MAYA_LOCATION + "/Python/Lib/plat-win")
sys.path.append(MAYA_LOCATION + "/Python/Lib/lib-tk")
print('\n'.join(sys.path))

maya.standalone.initialize()(name='python')


def export_fbx(_input_folder, _output_folder):
    # 获取指定文件夹内的所有.mb文件
    files = [f for f in os.listdir(_input_folder) if f.endswith('.mb')]

    for f in files:
        # 打开.mb文件
        file_path = os.path.join(_input_folder, f)
        cmds.file(file_path, force=True, open=True)

        # 导出.fbx文件
        fbx_path = os.path.join(_output_folder, f.replace('.mb', '.fbx'))
        cmds.file(fbx_path, force=True, options='fbx', type='FBX export', preserveReferences=False,
                  exportSelected=False)

    maya.standalone.uninitialize()


if __name__ == '__main__':
    input_folder = '/path/to/input/folder'
    output_folder = '/path/to/output/folder'
    export_fbx(input_folder, output_folder)
