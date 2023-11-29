- [mayaPython案例](#mayapython案例)
  - [选择骨骼层级](#选择骨骼层级)
  - [蒙皮和绑定姿态](#蒙皮和绑定姿态)
  - [通过模型获取蒙皮骨骼](#通过模型获取蒙皮骨骼)
  - [关于两点之间的距离](#关于两点之间的距离)
  - [获取骨骼链中所有骨骼](#获取骨骼链中所有骨骼)
  - [获取skinCluster](#获取skincluster)
  - [pymel中链接节点](#pymel中链接节点)
  - [属性接口连接信息查询，pm.connectionInfo()](#属性接口连接信息查询pmconnectioninfo)
  - [mel2py](#mel2py)
  - [矩阵](#矩阵)
  - [maya时间设置](#maya时间设置)
  - [maya 轴向](#maya-轴向)
  - [查找动画曲线并删除,直接删除位移缩放旋转曲线](#查找动画曲线并删除直接删除位移缩放旋转曲线)
  - [通过断开属性接口链接删除动画，推荐使用](#通过断开属性接口链接删除动画推荐使用)
  - [根据长名称获取骨骼列表的父子关系](#根据长名称获取骨骼列表的父子关系)
  - [获得maya所有全局变量](#获得maya所有全局变量)
  - [hik](#hik)
  - [Python 将字符串作为代码执行](#python-将字符串作为代码执行)
  - [关于fileDialog2](#关于filedialog2)
  - [inViewMessage](#inviewmessage)
  - [动画曲线过滤器](#动画曲线过滤器)
  - [获取模型的点线面](#获取模型的点线面)
# mayaPython案例
## 选择骨骼层级
```python
import pymel.core as pm
selection = pm.selected() #根骨骼放入变量
joints = pm.ls(selection[0], dag=True, type="joint") #列出骨骼链的所有骨骼，注意参数dag
pm.select(joints)#选择所有骨骼
```
## 蒙皮和绑定姿态
```python  
import pymel.core as pm
#蒙皮的启用与关闭
pm.skinCluster('skinCluster2', moveJointsMode=0, edit=True)
#选择所有骨骼
jntList = pm.ls(sl=True,dag=True,type="joint")
pm.select(jntList)
#查询绑定姿态
dagPose = pm.dagPose(bindPose=True,q=True)
#删除所有绑定姿势
pm.delete(dagPose)
#保存当前绑定姿态
pm.dagPose(bindPose=True,save=True)
#为蒙皮模型添加tweak调整节点，使模型蒙皮后仍可以调整点
pm.deformableShape('SK_Human_Male_001', createTweakNode=0)

pm.dagPose(name="rest",save=True)  # 储存dagpose
pm.dagPose(name="rest",restore=True)  # 返回dagpose
```
## 通过模型获取蒙皮骨骼
```python
import pymel.core as pm

def get_skinned_joints(model_name):
    """
    获取参与模型蒙皮的骨骼列表
    :param model_name: str, 模型的名称
    :return: list, 参与蒙皮的所有骨骼列表
    """
    # 获取模型节点
    model = pm.PyNode(model_name)

    # 获取模型的蒙皮集群节点列表
    skin_clusters = pm.listConnections(model, type='skinCluster')

    # 如果模型未绑定到任何集群，则返回空列表
    if not skin_clusters:
        return []

    # 获取集群的所有骨骼，并将其添加到骨骼列表中
    skin_joints = []
    for cluster in skin_clusters:
        joint_list = pm.skinCluster(cluster, q=True, inf=True)
        skin_joints.extend(joint_list)

    return list(set(skin_joints))
```
## 关于两点之间的距离
```python
#测量两点之间距离函数1
def getDisVal(point1,point2):
    Ax,Ay,Az = point1.getTranslation(space='world')
    Bx,By,Bz = point2.getTranslation(space='world')
    distance = ((Ax-Bx)**2+(Ay-By)**2+(Az-Bz)**2)**0.5
    return distance
#测量两点之间距离函数2
def getDisVal2(point1,point2):
    startPoint = point1.getTranslation(space='world')
    endPoint = point2.getTranslation(space='world')
    disShape = pm.distanceDimension(sp=startPoint,ep=endPoint)
    disVal = disShape.distance.get()
    pm.delete(disShape.getParent())
    return disVal
#测量两点之间距离函数3
def getDisVal3(point1,point2):
    pos1 = point1.getTranslation(space='world')  # 获取骨骼位置向量
    pos2 = point2.getTranslation(space='world')  # 获取其他骨骼向量
    distance = (pos1 - pos2).length()  # 获取两向量之差的长度
    return distance
#创建尾部骨骼
'''
def createjntchain(point1,point2,jointCount,chainName,direction=1):
    disVal = getDisVal(point1,point2)
    jntChainList = []
    for i in range(jointCount):
        tempJnt = pm.joint(n='{}_{}_JNT'.format(chainName,i+1),p=(0,0,(disVal/(jointCount-1)*i*direction)))
        jntChainList.append(tempJnt)
    pm.joint(jntChainList[0],zso=1, ch=1, e=1, oj='xyz', secondaryAxisOrient='yup')
    pm.joint(jntChainList[-1],zso=1,e=1, oj='none')
    pm.select(cl=True)
    return jntChainList
tailChainList = createjntchain(tailRoot,tailEnd,5,'tail',-1)
pointMatch(tailChainList[0],tailRoot)
'''
```
## 获取骨骼链中所有骨骼
```python
import pymel.core as pm

selection = pm.selected() #根骨骼放入变量
joints = pm.ls(selection[0], dag=True, type="joint") #列出骨骼链的所有骨骼，注意参数dag
pm.select(joints)#选择所有骨骼
```
## 获取skinCluster
```python
import pymel.core as pm

jnt = pm.selected()[0]#选择骨骼
skinCluster2 = pm.listConnections(jnt, type='skinCluster')#通过骨骼选择蒙皮节点

obj = pm.selected()[0]#选择模型
skinCluster1 = pm.listHistory(obj,type='skinCluster')#通过模型选择蒙皮节点
```
```python
import pymel.core as pm
jnt = pm.joint()
sphere, = pm.polySphere(ch=0)
pm.select(jnt,sphere)
pm.mel.SmoothBindSkin()
print (pm.mel.findRelatedSkinCluster(sphere))
```
## pymel中链接节点
```python
tailEndIKCtrl.rotateZ.connect(tailIKTwistMUD.input1X) #链接
tailEndIKCtrl.rotateZ.disconnect(tailIKTwistMUD.input1X) #打断

tailEndIKCtrl.rotateZ >> tailIKTwistMUD.input1X #链接
tailEndIKCtrl.rotateZ // tailIKTwistMUD.input1X #打断
```
## 属性接口连接信息查询，pm.connectionInfo()
```python
import maya.cmds as cmds

# 创建两个对象，并连接属性
cone = cmds.cone()[0]
sphere = cmds.sphere()[0]
sphereTx = f'{sphere}.tx'
coneTz = f'{cone}.tz'
cmds.connectAttr(sphereTx, coneTz)

# 验证连接并打印源接口。

# 如果接口是连接的目标，则返回 true，否则返回 false。
if cmds.connectionInfo(coneTz, isDestination=True):
    # 如果指定的接口是目标，则此标志返回连接的源接口。如果没有则为空。
    source_plug = cmds.connectionInfo(coneTz, sourceFromDestination=True)
    print(f'Source: {source_plug}')

#  验证连接并打印出目标接口。

# 如果接口是连接的源接口，则返回 true，否则返回 false。
if cmds.connectionInfo(sphereTx, isSource=True):
    # 如果指定的接口是源接口，则此标志返回从源连接的目的接口列表。如果没有则为空。
    destinations = cmds.connectionInfo(sphereTx, destinationFromSource=True)
    for destination in destinations:
        print(destination)
```
## mel2py
```python
import pymel.tools.mel2py as mel2py
mel_command = 'setDrivenKeyframe "-currentDriver pCube1.translateY  pCube2.translateX";  
setDrivenKeyframe "-currentDriver pCube1.translateY pCube2.translateY";  
setDrivenKeyframe "-currentDriver pCube1.translateY pCube2.translateZ";'
pythonCode = mel2py.mel2pyStr(mel_command, pymelNamespace='pm')
print(pythonCode)
```
## 矩阵
```python
import pymel.core as pm
target = pm.PyNode('ParentGeo')
target_matrix = pm.xform(target, q=True, matrix=True)
cube = pm.PyNode('pCube1')
cube_matrix = cube.getMatrix()
cube.setMatrix(target_matrix)
```
## maya时间设置
```python
# 通过对象的动画获取动画首末帧
firstFrame = pm.findKeyframe(root,which="first")
lastFrame = pm.findKeyframe(root,which="last")
# 设置时间栏首末帧
pm.env.setMinTime(firstFrame)
pm.env.setMaxTime(lastFrame)

pm.playbackOptions(minTime=firstFrame, maxTime=lastFrame )
# 调整帧率
pm.currentUnit(time='ntscf')  # 60fps
pm.currentUnit(time='ntsc')  # 30 fps
pm.currentUnit(time='film')  # 24 fps
```
## maya 轴向
```python
import pymel.all as pm
pm.env.setUpAxis("z")
panel = str(pm.getPanel(withFocus=1))
pm.viewSet(
    pm.mel.hotkeyCurrentCamera(panel),
    animate=pm.optionVar(query='animateRoll'),
    home=1
    )
```
## 查找动画曲线并删除,直接删除位移缩放旋转曲线
```python
weapon_jnt = pm.PyNode("weapon_R")

translate_cv = weapon_jnt.listConnections(type="animCurveTL")
rotate_cv = weapon_jnt.listConnections(type="animCurveTA")
scale_cv = weapon_jnt.listConnections(type="animCurveTU")
try:
    pm.delete(translate_cv, rotate_cv, scale_cv)
except Exception as e:
    print(e)
```
## 通过断开属性接口链接删除动画，推荐使用
```python
import pymel.core as pm


def deleteConnection(plug):
    """
        Deletes the connection of the given plug.
        Parameters:
            plug (str): The plug to delete the connection for.
        Returns:
            None
    """
    # 如果接口是连接的目标，则返回 true，否则返回 false。参数isDestination：是连接目标
    if pm.connectionInfo(plug, isDestination=True):
        # 获取确切目标接口，如果没有这样的连接，则返回None。
        plug = pm.connectionInfo(plug, getExactDestination=True)
        readOnly = pm.ls(plug, readOnly=True)
        # 如果该属性为只读
        if readOnly:
            # 获取连接的源接口
            source = pm.connectionInfo(plug, sourceFromDestination=True)
            # 断开源接口和目标接口
            pm.disconnectAttr(source, plug)
        else:
            # 如果不为只读，则删除目标接口
            # inputConnectionsAndNodes: 如果目标接口为只读，则不会删除
            pm.delete(plug, inputConnectionsAndNodes=True)


if __name__ == "__main__":
    # 获取选择列表
    sel_list = pm.selected()
    # 遍历选择列表
    for obj in sel_list:
        # 列出可动画属性
        attrs = obj.listAnimatable()
        # 遍历可动画属性
        for attr in attrs:
            # 断开动画连接
            deleteConnection(f"{attr}")
```
## 根据长名称获取骨骼列表的父子关系
```python
def getRelParent(self,jnt_list,root):
    """getRelParent 根据长名称获取骨骼列表的父子关系

    :param jnt_list: 蒙皮骨骼列表
    :type jnt_list: list
    :param root: 根骨骼
    :type root: [pymel.core.nodetypes.Joint] 
    :return: 骨骼的父子关系
    :rtype: dict
    """    
    jnt_parent = {}
    for jnt in jnt_list:
        hi_tree = jnt.longName().split("|")[1:-1]
        parent = None
        while parent not in jnt_list:
            if not hi_tree: 
                parent = root
                break
            parent = pm.PyNode(hi_tree.pop())
        jnt_parent[jnt] = parent if parent != root else parent
    return jnt_parent
```
## 获得maya所有全局变量
```python
import pymel.core as pm
allGlobals = pm.mel.env()
allGlobals_sort = sorted(allGlobals)
print(allGlobals_sort)
```
## hik
```python
import pymel.core as pm

pm.mel.HIKCharacterControlsTool()  # 打开hik窗口
pm.mel.hikCreateDefinition()  # 打开自定义hik骨骼窗口
pm.mel.hikCreateControlRig()  # 创建控制装备

allCharacter = pm.optionMenuGrp("hikCharacterList", query=True, itemListLong=True)  # 获取所有角色
sourceChar = pm.menuItem(allCharacter[1], query=True, label=True)  # 获取角色标签名称

optMenu = "hikCharacterList|OptionMenu"  # 定义角色列表窗口变量
pm.optionMenu(optMenu, edit=True, select=2)  # 设置角色窗口内的角色
# hik更新
pm.mel.hikUpdateCurrentCharacterFromUI()
pm.mel.hikUpdateContextualUI()
pm.mel.hikUpdateCharacterMenu()
pm.mel.hikUpdateCharacterControlsUICallback()


allSource = pm.optionMenuGrp("hikSourceList", query=True, itemListLong=True)  # 获取所有动画源
sourceChar = pm.menuItem(allSource[1], query=True, label=True)  # 获取动画源标签名称
optMenu = "hikSourceList|OptionMenu"   # 定义动画源列表窗口变量
pm.optionMenu(optMenu, edit=True, select=1)  # 设置动画源窗口内的角色
# hik更新
pm.mel.hikUpdateCurrentSourceFromUI()
pm.mel.hikUpdateContextualUI()
pm.mel.hikControlRigSelectionChangedCallback()
```
## Python 将字符串作为代码执行
```python
import pymel.core as pm

def exec_code(): 
    LOC = """ 
    
pm.polyCube() 

"""
    exec(LOC) 
 
exec_code()
```
## 关于fileDialog2
    fileMode：指示对话框要返回的内容。 0 任何文件，无论是否存在。1 单个现有文件。2 目录的名称。目录和文件都会显示在对话框中。3 目录的名称。对话框中仅显示目录。4 然后是一个或多个现有文件的名称。
```python
import pymel.core as pm

basicFilter = "*.mb"
pm.fileDialog2(fileFilter=basicFilter, dialogStyle=2)

singleFilter = "All Files (*.*)"
pm.fileDialog2(fileFilter=singleFilter, dialogStyle=2)

multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)"
pm.fileDialog2(fileFilter=multipleFilters, dialogStyle=2)
```
## inViewMessage
    <hl>Sleep</hl>，表示高亮，High Light。
```python
import pymel.core as pm
pm.inViewMessage(
                amg="I Fond It Very Difficult To Get To <hl>Sleep</hl>...",
                alpha=0.5,
                dragKill=True,
                pos="midCenterTop", 
                fade=True 
)
```
## 动画曲线过滤器
```python
import pymel.all as pm
# 关闭缓存曲线覆盖
pm.bufferCurve(animation="keys", overwrite=False)  
# 指定要使用的过滤器类型。可用的过滤器有： 
# butterworth, euler (default) ,gaussian ,keyReducer ,peakRemover ,keySync ,resample ,simplify
pm.filterCurve(
selectedKeys=True, filter='butterworth', 
cutoffFrequency=7, samplingRate=30, keepKeysOnFrame=1
)
# 动画曲线与缓存曲线互换
pm.bufferCurve( animation='keys', swap=True ) 
# 缓存曲线被动画曲线覆盖
pm.bufferCurve( animation='keys', overwrite=True )  

# 简化动画曲线
cmds.simplify(
    "{0}.{1}".format(selectedobj, a),
    time=(time_s, time_e),
    timeTolerance=value,
    floatTolerance=value,
    valueTolerance=value,
)
```
## 获取模型的点线面
```python
import pymel.core as pm

sel_mesh = pm.selected()[0]
sel_shape = sel_mesh.getShape()
assert isinstance(sel_shape, pm.nodetypes.Mesh)
sel_faces = sel_shape.faces
sel_deges = sel_shape.edges
sel_vtxs = sel_shape.vtx
sel_normals = sel_shape.getNormals()
```