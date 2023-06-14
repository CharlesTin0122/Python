# -*- coding: utf-8 -*-
'''
@FileName    :   mGear_retargeting_hik.py
@DateTime    :   2023/06/14 11:35:48
@Author  :   Tian Chao 
@Contact :   tianchao0533@163.com
'''

import pymel.core as pm
from mgear.shifter import mocap_tools

#import fbx
import FBXSpecial(animaFiles[0])

#get start and end frames
start_frame = cmds.playbackOptions(q=1, min=1)
end_frame = cmds.playbackOptions(q=1, max=1)
zero_frame = start_frame-10

#set a tpose on the mocap source
cmds.currentTime(zero_frame)
for jnt in anim_jnts:
try:
cmds.setAttr(‘MOCAP:%s.rotate’%jnt, 0,0,0,type=‘double3’)
except:
pass
cmds.setAttr(‘MOCAP:%s.translate’%anim_jnts[0], 0,0,0, type=‘double3’)

#make hik for mocap skeleton
set_HumanIK(‘Mocap_HIK’, hik_info)
hikSetSource(‘Mocap_HIK’, 1)
mocap_tools.importSkeletonBiped()
mocap_tools.characterizeBiped()

#set current character
setCurrentCharacter(‘mGear_Mocap_interface’)
hikSetSource(‘mGear_Mocap_interface’, 2)