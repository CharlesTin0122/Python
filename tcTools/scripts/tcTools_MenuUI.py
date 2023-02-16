# -*- coding: utf-8 -*-
'''
@FileName    :   tcTools_MenuUI.py
@DateTime    :   2023/02/13 16:26:21
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm
import maya.mel as mel
import sys
import os
#确定菜单分类，获取菜单文件夹所在的路径，获取菜单文件夹所在路径
menuList = ['Animation','Rigging','TD']
currentFilePath = r'{}'.format(os.path.dirname(__file__))
ScriptPackagesPath = r'{}\ScriptPackages'.format(currentFilePath)
commPath = [r'{}\{}'.format(currentFilePath,folder) for folder in menuList]
commPath.append(ScriptPackagesPath)
print(commPath,ScriptPackagesPath)

#添加菜单文件夹路径到Python路径
for path in commPath:
	if path in sys.path:
		print('Already In Evn Path!')
	else:
		sys.path.append(path)
#添加菜单文件夹路径到Mel路径
for path in commPath:
	if path in os.environ['MAYA_SCRIPT_PATH']:
		print('Already In Evn Path!')
	else:
		os.environ['MAYA_SCRIPT_PATH'] = '{};{}'.format(path,os.getenv('MAYA_SCRIPT_PATH'))
#获取菜单和子菜单目录
menuItemList = []
for item in menuList:
	path = r'{}\{}'.format(currentFilePath,item)
	for parent,dirnames,filenames in os.walk(path):
		if filenames:
			itemlist = []
			for f in filenames:
				if f.split('.')[0] not in itemlist:
					itemlist.append(f.split('.')[0])
				menuItemList.append([item,itemlist])

listA = menuItemList
menuItemList = []
for i in listA:
	if i not in menuItemList:
		menuItemList.append(i)

print(menuItemList)

#创建菜单
def createMenu(*args):
	if pm.menu('myMenu',ex=True):
		pm.deleteUI('myMenu')
	gMainWindow = mel.eval('$tmpVar=$gMainWindow')
	myMenu = pm.menu('myMenu',label ='tcTools',p=gMainWindow,tearOff=True)

	for menuItem in menuItemList:
		pm.menuItem(
			'{}_mItem'.format(menuItem[0]),
			label= menuItem[0],
			subMenu = True,
			p=myMenu,
			tearOff=True
			)
		for comm in menuItem[1]:
			pm.menuItem(
				'{}_mItem'.format(comm),
				label= comm,
				p='{}_mItem'.format(menuItem[0]),
				c='import {0};reload({0})'.format(comm)
				)

#删除菜单
def deleteMenu(*args):
	if pm.menu('myMenu',ex=True):
		pm.deleteUI('myMenu')



