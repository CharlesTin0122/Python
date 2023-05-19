# -*- coding: utf-8 -*-
# @FileName :  helloWorldCmd.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/5/11 9:50
# @Software : PyCharm
# Description:
import sys

import maya.OpenMayaMPx as OpenMayaMPx


# command
class HelloWorldCmd(OpenMayaMPx.MPxCommand):
    kPluginCmdName = "spHelloWorld"

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return OpenMayaMPx.asMPxPtr(HelloWorldCmd())

    def doIt(self, argList):
        print("Hello World!")


# Initialize the script plug-in
def initializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            HelloWorldCmd.kPluginCmdName, HelloWorldCmd.cmdCreator
        )
    except:
        sys.stderr.write(
            "Failed to register command: %s\n" % HelloWorldCmd.kPluginCmdName
        )
        raise


# Uninitialize the script plug-in
def uninitializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(HelloWorldCmd.kPluginCmdName)
    except:
        sys.stderr.write(
            "Failed to unregister command: %s\n" % HelloWorldCmd.kPluginCmdName
        )
        raise
