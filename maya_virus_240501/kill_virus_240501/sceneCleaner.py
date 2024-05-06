#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sceneClean
import maya.api.OpenMaya as omapi


def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


def after_open_callback(*args):
    sceneClean.delete_unknown_plugin_node()
    sceneClean.clear_bad_scripts()


def before_save_callback(*args):
    sceneClean.clear_bad_script_jobs()


def remove_scene_callback():
    if sceneClean.AFTER_OPEN_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.AFTER_OPEN_CALLBACK_ID)
        sceneClean.AFTER_OPEN_CALLBACK_ID = None

    if sceneClean.BEFORE_SAVE_CALLBACK_ID:
        omapi.MSceneMessage.removeCallback(sceneClean.BEFORE_SAVE_CALLBACK_ID)
        sceneClean.BEFORE_SAVE_CALLBACK_ID = None


def add_scene_callback():
    remove_scene_callback()
    sceneClean.AFTER_OPEN_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kAfterOpen, after_open_callback
    )
    sceneClean.BEFORE_SAVE_CALLBACK_ID = omapi.MSceneMessage.addCallback(
        omapi.MSceneMessage.kBeforeSave, before_save_callback
    )


def initializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject, "sceneCleanner", "1.1", "panyu&andy")
    add_scene_callback()


def uninitializePlugin(mobject):
    plugin = omapi.MFnPlugin(mobject)
    remove_scene_callback()
