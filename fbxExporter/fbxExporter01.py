import maya.cmds as cmds
import os

# set the path for the directory to export FBX files to
export_dir = 'path/to/export/directory'

# get a list of all the Maya files in the directory
maya_files = [f for f in os.listdir(export_dir) if f.endswith('.ma') or f.endswith('.mb')]

# loop over each Maya file and export it as an FBX file
for maya_file in maya_files:
    # open the Maya file
    cmds.file(os.path.join(export_dir, maya_file), open=True)

    # set the path for the FBX file to be exported
    fbx_file_path = os.path.join(export_dir, os.path.splitext(maya_file)[0] + '.fbx')

    # select the objects to be exported
    objects_to_export = cmds.ls(selection=True)

    # export the selected objects as an FBX file
    cmds.file(fbx_file_path, force=True, options="v=0", type="FBX export", pr=True, es=True, s=True, f=True)

    # close the Maya file
    cmds.file(force=True, close=True)
