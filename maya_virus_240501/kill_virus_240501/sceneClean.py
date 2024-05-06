#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import os
import shutil
import maya.cmds as cmds
import maya.mel as mm


JOB_INDEX_REGEX = re.compile(r"^(\d+):") # 正则表达式，表示 数字+：,例如：`13:`
'''
re.compile() 函数用于将正则表达式编译为可重用的对象。这使正则表达式匹配更有效率。
^: 此字符匹配字符串的开头。
(\d+): 此组捕获一个或多个数字(0-9)。括号创建了一个捕获组，这意味着匹配的字符将存储在变量中以供以后使用。
:: 此字符匹配一个字面冒号（:）。
$: 此字符匹配字符串的结尾。
'''
BAD_JOD_SCRIPTS = ["leukocyte.antivirus()"]

AFTER_OPEN_CALLBACK_ID = None
BEFORE_SAVE_CALLBACK_ID = None


def find_bad_scripts():
    """
    Finds and returns a list of script nodes in the current Maya scene that contain suspicious strings.

    Returns:
        list: A list of script nodes that contain suspicious strings.
    """
    bad_script_nodes = [] # 创建变量用于接收结果
    script_nodes = cmds.ls(type="script") # 获取场景中的所有脚本文件
    # 遍历场景中的脚本文件
    for script_node in script_nodes:
        # 判断脚本文件是否被引用，如果是则跳过
        if cmds.referenceQuery(script_node, isNodeReferenced=True):
            continue
        script_before_string = cmds.getAttr("{}.before".format(script_node)) # 获取脚本文件的before属性
        script_after_string = cmds.getAttr("{}.after".format(script_node)) # 获取脚本文件的after属性
        # 遍历脚本文件的before和after属性
        for script_string in [script_before_string, script_after_string]: 
            # 如果脚本字符串为空，则跳过
            if not script_string: 
                continue
            # 如果脚本字符串包含以下关键字，则将脚本文件添加到bad_script_nodes列表中
            if (
                "internalVar" in script_string
                or "userSetup" in script_string
                or "fuckVirus" in script_string
                or 'python("import base64; _pycode = base64.urlsafe_b64decode'
                in script_string
            ):
                bad_script_nodes.append(script_node)
    # 返回脚本节点
    return bad_script_nodes 


def del_bad_scripts(bad_script_nodes):
    """
    Deletes the provided script nodes by unlocking them and deleting them.

    Parameters:
        bad_script_nodes (list): A list of script nodes to be deleted.

    Returns:
        None
    """
    # 遍历所有提供的参数节点，解除锁定并删除节点。
    for bad_script_node in bad_script_nodes:
        cmds.lockNode(bad_script_node, l=False)
        cmds.delete(bad_script_node)


def clear_bad_scripts():
    """
    Clears bad script nodes from the Maya scene.
    """
    bad_script_nodes = find_bad_scripts() # 找到病毒节点
    if not bad_script_nodes:
        # 如果病毒节点不存在，则返回
        return
    # 删除病毒节点
    del_bad_scripts(bad_script_nodes)
    # 删除本地可疑文件
    delete_local_file()
    # 弹出确认对话框
    cmds.confirmDialog(
        title="Found these suspicious nodes!",
        message="Delete these Script nodes:\n    {}".format(
            "\n    ".join(bad_script_nodes)
        ),
        button="OK",
    )


def find_bad_script_jobs(bad_jod_scripts=BAD_JOD_SCRIPTS):
    """
    Finds bad script jobs based on a list of bad job scripts.

    Parameters:
        bad_jod_scripts (list): A list of bad job scripts to search for in the script jobs.

    Returns:
        list: A list of bad script jobs found based on the bad job scripts.
    """
    bad_script_jobs = [] # 创建变量用于接收结果
    script_jobs = cmds.scriptJob(listJobs=True) # 列出所有的script Job
    for script_job in script_jobs: # 遍历所有的script Job
        for bad_jod_script in bad_jod_scripts: # 遍历所有的参数提供的bad job script
            # 如果场景script jobs中包含参数提供的bad job script，则将script job添加到bad_script_jobs列表中
            if bad_jod_script in script_job:
                bad_script_jobs.append(script_job)
    return bad_script_jobs # 返回可疑script jobs列表


def del_bad_script_jobs(bad_script_jobs):
    """
    Deletes the specified bad script jobs.

    Args:
        bad_script_jobs (list): A list of bad script jobs to be deleted.

    Returns:
        None

    This function iterates over each bad script job in the `bad_script_jobs` list and extracts the script job index using the `JOB_INDEX_REGEX` regular expression. 
    It then uses the `cmds.scriptJob` function to kill the corresponding script job with the extracted index. 
    The `force` parameter is set to `True` to force the deletion of the script job.
    """

    for bad_script_job in bad_script_jobs: # 遍历参数提供的script jobs 
        '''
        findall(): 该方法在给定的字符串bad_script_job中查找正则表达式JOB_INDEX_REGEX模式的所有匹配项
        int():将提取的作业索引（它是一个字符串）转换为整数数据类型。
        '''
        bad_script_job_index = int(JOB_INDEX_REGEX.findall(bad_script_job)[0]) # 使用正则表达式提取脚本作业索引
        cmds.scriptJob(kill=bad_script_job_index, force=True) # 强行终止移除该script job


def clear_bad_script_jobs():
    """清除可疑的script jobs
    """
    bad_script_jobs = find_bad_script_jobs() # 找到可疑的script jobs
    if not bad_script_jobs: # 如果可疑的script jobs不存在，则返回
        return
    del_bad_script_jobs(bad_script_jobs) # 删除可疑的script jobs
    delete_local_file() # 删除本地可疑文件
    # 弹出确认对话框
    cmds.confirmDialog( 
        title="Found these suspicious jobs!",
        message="Delete these Script jobs:\n    {}".format(
            "\n    ".join(bad_script_jobs)
        ),
        button="OK",
    )


def delete_local_file():
    """
    Deletes local files related to the vaccine and fuckVirus Python scripts.
    删除`X:/Documents/maya/`路径下这些文件
    - vaccine.py
    - vaccine.pyc
    - fuckVirus.py
    - fuckVirus.pyc
    - userSetup.py
    - userSetup.mel
    """
    # 获取要删除的文件路径储存为变量
    scriptsPath = "{}/scripts".format(cmds.internalVar(userAppDir=True)) # 
    vaccinePyPath = "{}/vaccine.py".format(scriptsPath)
    vaccinePycPath = "{}/vaccine.pyc".format(scriptsPath)
    fuckVirusPyPath = "{}/fuckVirus.py".format(scriptsPath)
    fuckVirusPycPath = "{}/fuckVirus.pyc".format(scriptsPath)
    vaccineUserSetupPath = "{}/userSetup.py".format(scriptsPath)
    baseVirus = "{}/userSetup.mel".format(scriptsPath)
    # 在 Python 中，os.path.expandvars() 函数用于解析路径中的环境变量。它会将路径中类似 $name 或 ${name} 形式的子字符串替换为对应的环境变量 name 的值。
    baseVirusF = os.path.expandvars(r"C:\Users\%USERNAME%\AppData\Roaming\syssst")
    vaccinePattern = "import vaccine"
    fuckVirusPattern = "import fuckVirus"
    # 删除指定可疑文件
    if os.path.exists(vaccinePyPath):
        print("delete vaccine.py\n")
        cmds.sysFile(vaccinePyPath, delete=True)

    if os.path.exists(vaccinePycPath):
        print("delete vaccine.pyc\n")
        cmds.sysFile(vaccinePycPath, delete=True)

    if os.path.exists(fuckVirusPyPath):
        print("delete fuckVirus.py\n")
        cmds.sysFile(fuckVirusPyPath, delete=True)

    if os.path.exists(fuckVirusPycPath):
        print("delete fuckVirus.pyc\n")
        cmds.sysFile(fuckVirusPycPath, delete=True)
    
    if os.path.exists(vaccineUserSetupPath): # 如果userSetup.py文件存在
        # 读取文件内容，储存到allText变量中
        with open(vaccineUserSetupPath, "r") as f:
            allText = f.read()
            f.close()
        # 如果文件内容中包含vaccine或fuckVirus字符串，则删除userSetup.py
        if vaccinePattern in allText or fuckVirusPattern in allText:
            print("delete error userSetup.py")
            cmds.sysFile(vaccineUserSetupPath, delete=True)

    if os.path.exists(baseVirus): # 如果userSetup.mel文件存在
        # 读取文件内容，储存到allText变量中
        with open(baseVirus, "r") as f: 
            allText = f.read()
            f.close()
        # 如果文件内容中包含可疑字符串，则删除userSetup.mel
        if 'python("import base64; pyCode = base64.urlsafe_b64decode' in allText:
            print("delete error {}".format(baseVirus))
            cmds.sysFile(baseVirus, delete=True)
    # 如何该路径"C:\Users\%USERNAME%\AppData\Roaming\syssst"存在，删除它
    if os.path.exists(baseVirusF):
        print("delete {}\n".format(baseVirusF))
        # 递归删除整个目录树。它可以高效地清除指定目录中的所有文件和子目录，彻底清理整个文件夹结构。
        shutil.rmtree(baseVirusF)


def delete_unknown_plugin_node():
    unknownNode = cmds.ls(type="unknown") # 列出场景中的未知节点
    unknownPlugin = cmds.unknownPlugin(query=True, l=True) # 列出未知插件

    if unknownNode: # 如果未知节点存在
        for nodeObj in unknownNode: # 遍历未知节点
            if cmds.objExists(nodeObj): # 如果节点存在
                 # 如果节点是引用，则跳过
                if cmds.referenceQuery(nodeObj, isNodeReferenced=True):
                    cmds.warning("Node from refrence, skip.  {}".format(nodeObj))
                    continue
                if cmds.lockNode(nodeObj, query=True)[0]: # 如果节点被锁定
                    # 尝试解锁，如解锁失败则警告并跳过
                    try:
                        cmds.lockNode(nodeObj, lock=False)
                    except Exception as e:
                        cmds.warning(
                            "The node is locked and cannot be unlocked. skip  {}".format(
                                nodeObj
                            )
                        )
                        continue
                # 尝试删除未知节点
                try:
                    cmds.delete(nodeObj)
                    cmds.warning("Delete node :  {}".format(nodeObj))
                except Exception as e:
                    pass

    if unknownPlugin: # 如果未知插件存在
        # 遍历未知插件，移除除插件
        for plugObj in unknownPlugin: 
            cmds.unknownPlugin(plugObj, remove=True)
            cmds.warning("Delete plug-in :  {}".format(plugObj))


def fix_model_error():
    needs_fixing = False
    try:
        expression_str = cmds.getAttr("uiConfigurationScriptNode.before")
        fixed_expression_lines = []
        for line in expression_str.split("\n"):
            if '-editorChanged "onModelChange3dc"' in line:
                needs_fixing = True
                continue
            fixed_expression_lines.append(line)
        fixed_expression = "\n".join(fixed_expression_lines)
        if needs_fixing:
            cmds.setAttr(
                "uiConfigurationScriptNode.before", fixed_expression, typ="string"
            )
            cmds.warning("清理完毕")
    except:
        pass


def fix_callback_rrror():
    for modelPanel in cmds.getPanel(typ="modelPanel"):
        if (
            cmds.modelEditor(modelPanel, query=True, editorChanged=True)
            == "CgAbBlastPanelOptChangeCallback"
        ):
            cmds.modelEditor(modelPanel, edit=True, editorChanged="")
            cmds.warning("清理完毕")


def fix_look_error():
    mm.eval('outlinerEditor -edit -selectCommand "" "outlinerPanel1";')
    cmds.warning("清理完毕")
