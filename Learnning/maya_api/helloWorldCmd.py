# -*- coding: utf-8 -*-
# @FileName :  helloWorldCmd.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/11 9:50
# @Software : PyCharm
# Description:

import sys

import maya.OpenMayaMPx as OpenMayaMPx

kPluginCmdName = "spHelloWorld"


# command
class ScriptedCommand(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, argList):
        print("Hello World!")


# Creator
def cmd_creator():
    return OpenMayaMPx.asMPxPtr(ScriptedCommand())


# Initialize the script plug-in
def initialize_plugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(kPluginCmdName, cmd_creator)
    except:
        sys.stderr.write("Failed to register command: %s\n" % kPluginCmdName)
        raise


# Uninitialize the script plug-in
def uninitialize_plugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(kPluginCmdName)
    except:
        sys.stderr.write("Failed to unregister command: %s\n" % kPluginCmdName)
        raise
