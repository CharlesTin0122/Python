import ast
import maya.cmds as cmds


def return_attribute():
    """获得曲线编辑器中有动画的属性

    Returns:
        list: 曲线编辑器中有动画的属性
    """
    attr_list = []
    # 获得曲线编辑器中显示的所有属性，curvesShown参数返回一个字符串数组，包含当前曲线编辑器中所显示的曲线属性
    curves = cmds.animCurveEditor("graphEditor1GraphEd", curvesShown=True, q=True)
    # 在曲线编辑器中所显示的动画属性中，通过遍历所有属性，找到有动画信息的属性并将其装入attr_list变量
    for i in curves:
        # timeChange参数会返回所有有动画帧的时间点，使用这个参数可确定这个属性有没有动画。
        if cmds.keyframe(i.replace("_", "_"), sl=True, query=True, timeChange=True):
            attr_list.append(i.replace("_", "_"))
    # 返回曲线编辑器中有动画的属性
    return attr_list


def get_mytimes(attr):
    """
    获得给出属性的所有关键帧时间点

    Args:
        attr (str): 属性名称.

    Returns:
        list: 时间点列表.

    Example:
        >>> get_mytimes('translateX')
        [1, 2, 3, 4, 5]
    """
    # 获得给出属性的所有关键帧时间点，如果没有帧则为空列表
    mytimes = cmds.keyframe(attr, sl=True, query=True, timeChange=True) or []
    if len(mytimes) > 0:  # 如果时间点多余0个
        # 遍历最初时间点到最末时间点的每一帧，如果此帧上有动画帧则添加到mytimes列表中
        for x in range(int(mytimes[0]), int(mytimes[-1])):
            # valueChange参数可返回所有有动画帧的属性值
            if cmds.keyframe(attr, time=(x, x), valueChange=True, q=True):
                if x not in mytimes:
                    mytimes.append(x)
    # 返回有属性值变化的时间点列表
    return mytimes


def get_mykeys(attr):
    """
    检索指定属性的关键帧属性值。

    Args:
        attr (str): 要检索属性值的属性名称.

    Returns:
        list: 指定属性的关键帧属性值列表.
    """
    # valueChange参数可返回所有有动画帧的属性值，如果没有帧则为空列表
    mykeys = (
        cmds.keyframe(attr, sl=True, query=True, valueChange=True, absolute=True) or []
    )
    return mykeys


def get_dict(attr):
    """
    根据给出的属性创建一个字典，该字典以时间点为键，属性值为值.
    Args:
        attr (str): 要创建字典的属性名称.

    Returns:
        dict: 指定属性的字典.
    """
    dic = {}  # 创建一个空字典dic
    mykeys = get_mykeys(attr) or []  # 获取一个属性的关键帧属性值列表
    if len(mykeys) >= 3:  # 如果该列表的长度大于等于3，也就是关键帧数量大于3
        # 从函数调用get_mytimes(attr)获取一个时间值，并将mykeys中对应索引位置的值赋给变量cur_value，然后将时间作为键，cur_value作为值，添加到字典dic中。
        for index in range(1, len(mykeys) - 1):
            time = get_mytimes(attr)[index]  # 获得给出属性的关键帧时间点对应索引位置的值
            cur_value = mykeys[index]  # 获得属性值列表中对应索引位置的值
            dic[time] = cur_value  # 添加到字典dic中
    """
    optionVar()是 Maya Python API 中的一个函数，用于设置和获取 Maya 的选项变量（option variable）。
    选项变量是一种在 Maya 中存储和检索数据的方法，可以用于保存用户设置、配置信息等。
    以下代码创建一个名为 "mydict_{attr}" 的选项变量，并将字典 dic 的字符串表示作为其值进行设置。这可以在 Maya 中存储和检索该字典的值，以便在其他地方使用。
    """
    # stringValue参数，使用第一个字符串创建一个新变量，其值由第二个字符串给出。如果具有该名称的变量已存在，则该变量将被覆盖以支持新值（即使类型不同）
    cmds.optionVar(stringValue=(f"mydict_{attr}", str(dic)))
    return dic


def resample_keys(kv, thresh):
    """
    根据给定阈值对字典中的键重新采样。

    Args:
        kv (dict): 时间点为键，属性值为值的字典.
        thresh (float): 容错阈值.

    Returns:
        list: 包含重新采样的键值对的字典列表.

    Examples:
        >>> kv = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}
        >>> thresh = 5.0
        >>> resample_keys(kv, thresh)
        [{1.0: 10.0, 5.0: 50.0}]
    """
    if kv.keys():  # 代码检查字典kv是否有键。如果有键，代码将继续进行重新采样的过程。
        # 计算字典中最小和最大键的值，并将其作为开始和结束值
        start = float(min(kv.keys()))
        end = float(max(kv.keys()))
        # 计算开始和结束值的对应数值
        start_value = float(kv[start])
        end_value = float(kv[end])
        # 初始化了用于存储总误差、异常键和异常值的变量
        total_error = 0
        offender = -1
        outlier = -1
        # 遍历字典中的键值对
        for k, v in kv.items():
            if end - start != 0:
                # 根据当前键的位置与开始和结束键的关系计算时间比例
                time_ratio = (k - start) / (end - start)
                # 根据时间比例、开始值和结束值计算采样值
                sample = time_ratio * end_value + (1 - time_ratio) * start_value
                # 计算当前值与采样值之间的绝对差值（delta）
                delta = abs(v - sample)
                # 将其添加到总误差中
                total_error += delta
                # 如果delta大于当前异常值，代码更新异常值和异常键。
                if delta > outlier:
                    outlier = delta
                    offender = k
        # 检查总误差是否低于阈值，或者字典是否仅有两个键。如果满足任一条件，代码返回一个包含开始和结束键以及对应值的字典的列表
        if total_error < thresh or len(kv.keys()) == 2:
            return [{start: start_value, end: end_value}]
        # 如果不满足条件，代码根据异常键将字典分为两个子集，并对每个子集递归调用resample_keys函数。然后，代码返回两个递归调用的结果的连接。
        else:
            s1 = {kk: vv for kk, vv in kv.items() if kk <= offender}
            s2 = {kk: vv for kk, vv in kv.items() if kk >= offender}
            return resample_keys(s1, thresh) + resample_keys(s2, thresh)


def rejoin_keys(kvs):
    """
    这个函数的作用是将一个由多个字典组成的列表重新合并为一个单独的字典。
    它接受一个参数 kvs，该参数是一个字典列表。函数将遍历列表中的每个字典，并将它们合并到一个新的字典中，最后返回这个新的字典作为结果。

    Args:
        kvs (list[dict]): 要重新加入的词典列表

    Returns:
        dict: 重新加入所有字典后得到的字典.
    """
    result = {}
    # 迭代遍历 kvs 中的每个字典。它使用 update 方法将这些字典合并到 result 中
    for item in kvs:
        result.update(item)
    # 返回合并后的字典
    return result


def decimate(attr, tolerance):
    """
    通过重采样给定的属性字典生成新字典.

    Args:
        attr (str): 要重采样的属性.
        tolerance (float): 重采样容差值.

    Returns:
        dict: 重采样后的字典.
    """
    """
    ast.literal_eval() 是 Python 中的一个函数，用于将字符串表示的字面值转换为它们对应的 Python 数据类型。
    它可以安全地评估字符串中的字面值，包括数字、字符串、列表、元组和字典，而不会执行任何其他代码。
    这个函数通常用于处理从外部源（如用户输入或配置文件）获取的字符串，以确保安全性和避免潜在的安全漏洞。
    """
    # 将选项变量（option variable）中的字符串转换成对应的 Python 数据类型
    mydict = ast.literal_eval(cmds.optionVar(q="mydict_{0}".format(attr)))
    # 返回重采样并合并后的字典
    return rejoin_keys(resample_keys(mydict, tolerance))


def resample(attr, tolerance, mytimes):
    """
    根据提供的容差对给定属性重新采样.
    总结起来，这段代码根据容差值重新采样给定属性（attr）的关键帧。
    它通过比较现有关键帧时间（mytimes）和由 decimate 函数生成的新关键帧时间（newtimes）来添加或删除关键帧。

    Parameters:
        attr (str): 要重采样的属性名称.
        tolerance (float): 用于重采样的容差值.
        mytimes (list): 与属性关联的时间列表.

    Returns:
        None
    """
    mytimes = get_mytimes(attr)  # 获取属性的关键帧时间点
    mytimes.sort()  # 对 mytimes 列表进行排序。
    # 使用 attr 和 tolerance 参数调用一个名为 decimate 的函数，该函数返回一个名为 resample_dict 的字典。
    resample_dict = decimate(attr, tolerance)
    newtimes = resample_dict.keys()  # 提取 resample_dict 的键
    newtimes.sort()  # 将其排序成一个名为 newtimes 的新列表
    # 从 mytimes 列表中移除第一个和最后一个元素。
    mytimes.pop(0)
    mytimes.pop(-1)
    # 检查 mytimes 的长度是否大于 newtimes 的长度
    # 如果是，遍历一个列表，其中包含在 mytimes 或 newtimes 中但不在两者之间的元素，并调用一个名为 cmds.cutKey 的函数来删除这些时间值对应的关键帧。
    if len(mytimes) > len(newtimes):
        for t in [
            i for i in mytimes + newtimes if i not in mytimes or i not in newtimes
        ]:
            cmds.cutKey(attr, time=(t, t), option="keys")
    # 如果 mytimes 的长度小于 newtimes 的长度，则遍历一个类似的列表，并调用 cmds.setKeyframe 和 cmds.keyframe 函数来设置关键帧并更新其值。
    elif len(mytimes) < len(newtimes):
        for x in [
            i for i in mytimes + newtimes if i not in mytimes or i not in newtimes
        ]:
            cmds.setKeyframe(attr, t=x)
            cmds.keyframe(attr, time=(x, x), valueChange=resample_dict[x])


def record():
    """
    获得曲线编辑器中属性动画曲线字典的函数.
    Returns:
        None
    """
    # 调用return_attribute函数获取属性列表，对每个属性进行迭代
    for attr in return_attribute():
        mytimes = get_mytimes(attr)  # 获得属性的关键帧时间点
        if len(mytimes) > 0:  # 如果 mytimes 的长度大于 0
            get_dict(attr)  # 获得属性的动画曲线字典


def resampleDrag(value, tolerance_value):
    """
    根据给拖动值和公差值对动画曲线重新采样.

    Parameters:
    - value: 拖动值.
    - tolerance_value: 用于对拖动值重新采样的容差值.

    Returns:
    None
    """
    # 调用return_attribute()函数返回的属性进行迭代
    for attr in return_attribute():
        mytimes = get_mytimes(attr)  # 获取相应的mytimes
        if len(mytimes) > 0:  # 如果有的话
            # 使用属性、拖动值除以及容差值的结果以及mytimes作为参数调用了一个名为resample的函数
            # 主要用于在UI界面拖动属性滑条来进行动画曲线的重采样
            resample(attr, value / float(tolerance_value), mytimes)


def pre_key(i, a):
    """
    检索给定对象在当前时间的指定属性的前一个关键帧值。

    参数：
        i (str)：对象的名称。
        a (str)：属性的名称。

    返回值：
        给定对象在当前时间的指定属性的前一个关键帧值。
    """
    # 使用cmds.currentTime(query=True)获取当前时间
    current_time = cmds.currentTime(query=True)
    # 使用cmds.findKeyframe()找到给定对象和属性（i和a）的上一个关键帧
    previous_time = cmds.findKeyframe(
        "{0}.{1}".format(i, a), time=(current_time, current_time), which="previous"
    )
    # 使用cmds.keyframe()获取上一个关键帧的值，通过指定上一个关键帧的时间并对其进行评估
    previous_key = cmds.keyframe(
        "{0}.{1}".format(i, a),
        time=(previous_time, previous_time),
        query=True,
        eval=True,
    )
    # 返回上一个关键帧的值
    return previous_key


def next_key(i, a):
    """
    返回给定对象和属性在当前时间的下一个关键帧值。

    参数：
        i (str)：对象的名称或路径。
        a (str)：属性的名称。

    返回：
        float：如果存在下一个关键帧，则返回其值，否则返回 None。
    """

    current_time = cmds.currentTime(query=True)
    next_time = cmds.findKeyframe(
        "{0}.{1}".format(i, a), time=(current_time, current_time), which="next"
    )
    next_key = cmds.keyframe(
        "{0}.{1}".format(i, a), time=(next_time, next_time), query=True, eval=True
    )
    return next_key


def pre_key_time(i, a):
    """
    在当前时间中查找指定对象属性的上一个关键帧时间。

    Args:
        i (str): 对象名称。
        a (str): 属性名称。

    Returns:
        float: 上一个关键帧的时间，如果不存在上一个关键帧则返回 None。
    """

    current_time = cmds.currentTime(query=True)
    previous_time = cmds.findKeyframe(
        "{0}.{1}".format(i, a), time=(current_time, current_time), which="previous"
    )
    return previous_time


def next_key_time(i, a):
    """
    找到给定对象和属性的下一个关键帧时间。

    参数：
        i (str): 对象的名称。
        a (str): 属性的名称。

    返回：
        float: 指定对象和属性的下一个关键帧的时间。
    """

    current_time = cmds.currentTime(query=True)
    next_time = cmds.findKeyframe(
        "{0}.{1}".format(i, a), time=(current_time, current_time), which="next"
    )
    return next_time


def twinner(value):
    """
    计算每个选择对象在当前时间上指定属性的插值关键帧值。

    Args：
        value（float）：要计算插值关键帧值的百分比值。

    Returns：
        无
    """

    current_time = cmds.currentTime(query=True)  # 获取当前时间
    list = cmds.ls(selection=True)  # 获取所选对象的列表
    # 对每个对象进行迭代以查找可关键帧的属性
    for i in list:
        attr = cmds.listAttr(i, keyable=True)
        # 对于每个属性，它检查当前时间是否存在关键帧
        for a in attr:
            # 如果前时间属性存在
            if cmds.objExists("{0}.{1}".format(i, a)):
                # 则获取当前属性当前时间点的关键帧属性值
                current_value = cmds.keyframe(
                    "{0}.{1}".format(i, a),
                    time=(current_time, current_time),
                    query=True,
                    eval=True,
                )
                # 如果属性值存在则获取前一个关键帧和后一个关键帧的属性值
                if current_value:
                    pre_value = pre_key(i, a)
                    next_value = next_key(i, a)
                    # 如果前一个关键帧和后一个关键帧的属性值存在
                    if pre_value and next_value:
                        # 如果前一个关键帧和后一个关键帧的属性值存在，并且当前属性在当前时间没有关键帧
                        if not cmds.keyframe(
                            "{0}.{1}".format(i, a),
                            time=(current_time, current_time),
                            q=True,
                        ):
                            # 则设置关键帧
                            cmds.setKeyframe("{0}.{1}".format(i, a), t=current_time)
                        """
                        在这段代码中，检查next_value列表的第一个元素是否不等于current_value是为了确定是否需要进行差值计算。
                        如果next_value列表的第一个元素与current_value相等，那么就没有必要进行差值计算，因为新值将与当前值保持一致。
                        只有在next_value列表的第一个元素与current_value不相等时，才需要进行差值计算来生成一个新的值。
                        """
                        # 如果前一个关键帧和后一个关键帧的属性值存在，并且下一个关键帧与当前关键帧不同
                        if next_value[0] != pre_value:
                            # 根据前一个关键帧和后一个关键帧的值，差值计算一个新值
                            key_value = (
                                value / 100.0 * (next_value[0] - pre_value[0])
                                + pre_value[0]
                            )
                            # 更新关键帧的值
                            cmds.keyframe(
                                "{0}.{1}".format(i, a),
                                time=(current_time, current_time),
                                valueChange=key_value,
                            )


def scalekey(perscentage):
    """
    根据给定的百分比，缩放所选对象的关键帧。
    其原理是：将首尾两帧连线,找出曲线上每一帧投射到连线上的值, 已此值作为pivot来对对应的曲线上的点进行缩放.

    Args:
        perscentage (float): 缩放关键帧的百分比。

    Returns:
        None
    """
    # 获取选择的对象列表
    selectedobjList = cmds.ls(sl=True)
    # 遍历每个选择的对象
    for selectedobj in selectedobjList:
        # 获取对象的可关键属性
        Attr = cmds.listAttr(selectedobj, keyable=True)
        # 遍历每个属性
        for a in Attr:
            # 获取属性关键帧的值
            mykeys = (
                cmds.keyframe(
                    "{0}.{1}".format(selectedobj, a),
                    sl=True,
                    query=True,
                    valueChange=True,
                    absolute=True,
                )
                or []
            )
            # 获取属性关键帧的时间
            timechange = (
                cmds.keyframe(
                    "{0}.{1}".format(selectedobj, a),
                    sl=True,
                    query=True,
                    timeChange=True,
                    absolute=True,
                )
                or []
            )
            # 检查是否至少有2个具有值和时间变化的关键帧
            if len(mykeys) >= 2 and len(timechange) >= 2:
                # 根据第一个和最后一个关键帧的值和时间变化计算切线，切线等于首末帧值差除以首末帧时间差
                tangent = (mykeys[-1] - mykeys[0]) / abs(timechange[-1] - timechange[0])
                index = 1
                # 从第二个关键帧开始遍历关键帧
                while index < len(mykeys) - 1:
                    # 获取关键帧的时间
                    time = cmds.keyframe(
                        "{0}.{1}".format(selectedobj, a),
                        selected=True,
                        query=True,
                        timeChange=True,
                    )[index]
                    # 根据切线和时间差计算缩放中心点
                    # 切线乘以时间差可以得到从第一个关键帧到当前关键帧的属性值变化量，然后再加上第一个关键帧的属性值，就可以得到当前关键帧的缩放中心点位置。
                    scalePivot = tangent * (time - timechange[0]) + mykeys[0]
                    # 使用缩放中心点和百分比缩放关键帧
                    cmds.scaleKey(
                        "{0}.{1}".format(selectedobj, a),
                        time=(time, time),
                        valuePivot=scalePivot,
                        valueScale=perscentage,
                    )
                    index = index + 1
    """
    关键帧之间的切线表示属性值的变化率。计算切线是为了确定在关键帧之间进行缩放时，属性值的变化率。

    算法的步骤如下：

    1.获取关键帧的值变化列表 mykeys 和时间变化列表 timechange。
    2.计算切线 tangent，使用公式 tangent = (mykeys[-1] - mykeys[0]) / abs(timechange[-1] - timechange[0])。
    这个公式计算的是第一个关键帧和最后一个关键帧之间的平均变化率，即切线。
    3.遍历每个关键帧，通过以下步骤计算缩放中心点的位置：
    4.获取当前关键帧的时间 time。
    5.计算时间差 time - timechange[0]，表示当前关键帧相对于第一个关键帧的时间差。
    6.将时间差乘以切线 tangent，得到从第一个关键帧到当前关键帧的属性值变化量。
    7.将属性值变化量加上第一个关键帧的属性值 mykeys[0]，得到当前关键帧的缩放中心点位置。

    通过这个算法，可以根据关键帧之间的切线和时间差，计算出在关键帧之间进行缩放时的缩放中心点的位置。这样可以实现对关键帧进行精确的缩放操作。
    """


def smooth():
    """
    平滑选定对象的动画曲线.

    Returns:
        None
    """
    # 获取选定对象的列表
    selectedobjList = cmds.ls(sl=True)
    # 遍历每个选定对象
    for selectedobj in selectedobjList:
        # 获取选定对象的可关键属性列表
        Attr = cmds.listAttr(selectedobj, keyable=True)
        # 遍历每个属性
        for a in Attr:
            # 获取属性的关键帧值列表
            mykeys = (
                cmds.keyframe(
                    "{0}.{1}".format(selectedobj, a),
                    sl=True,
                    query=True,
                    valueChange=True,
                    absolute=True,
                )
                or []
            )
            # 检查是否至少有3个关键帧
            if len(mykeys) >= 3:
                index = 1
                # 遍历每个关键帧索引
                while index < len(mykeys) - 1:
                    # 获取当前关键帧的时间
                    time = cmds.keyframe(
                        "{0}.{1}".format(selectedobj, a),
                        sl=True,
                        timeChange=True,
                        query=True,
                    )[index]
                    # 获取前一个、当前和下一个关键帧的值
                    pre_value = mykeys[index - 1]
                    cur_value = mykeys[index]
                    nex_value = mykeys[index + 1]
                    # 计算前一个、当前和下一个值的平均值
                    average = (pre_value + cur_value + nex_value) / 3
                    # 将当前关键帧的值设为计算得到的平均值
                    cmds.keyframe(
                        "{0}.{1}".format(selectedobj, a),
                        time=(time, time),
                        valueChange=average,
                    )
                    index = index + 1


def simplify_(perscentage):
    """
    根据给定的百分比容差简化所选对象属性的关键帧。

    Args:
        percentage (float): 关键帧简化的容差百分比。

    Returns:
        None
    """
    value = perscentage / 100.0
    # 获取当前选中对象的列表
    selectedobjList = cmds.ls(sl=True)
    # 遍历每个选中对象
    for selectedobj in selectedobjList:
        # 获取选中对象的可关键属性列表
        Attr = cmds.listAttr(selectedobj, keyable=True)
        # 遍历每个可关键属性
        for a in Attr:
            # 获取属性的关键帧时间值
            mytimes = (
                cmds.keyframe(
                    "{0}.{1}".format(selectedobj, a),
                    sl=True,
                    query=True,
                    timeChange=True,
                    absolute=True,
                )
                or []
            )
            # 检查属性是否有关键帧
            if len(mytimes) > 0:
                # 获取关键帧的起始时间和结束时间
                time_s = mytimes[0]
                time_e = mytimes[-1]
                # 打印起始时间和结束时间以进行调试
                print(time_s)
                print(time_e)
                # 在给定的时间范围内简化属性的关键帧
                cmds.simplify(
                    "{0}.{1}".format(selectedobj, a),
                    time=(time_s, time_e),
                    timeTolerance=value,
                    floatTolerance=value,
                    valueTolerance=value,
                )
                # 选择简化后的关键帧
                cmds.selectKey("{0}.{1}".format(selectedobj, a), time=(time_s, time_e))


def butterworth(perscentage):
    """
    对所选对象的动画曲线应用 Butterworth 滤波器。

    参数:
        perscentage (float): 缩放动画曲线值的百分比。
    """
    # 获取所选对象列表
    selectedobjList = cmds.ls(sl=True)
    # 遍历每个所选对象
    for selectedobj in selectedobjList:
        # 获取当前对象的可关键属性列表
        Attr = cmds.listAttr(selectedobj, keyable=True)
        # 遍历每个可关键属性
        for a in Attr:
            # 获取当前属性的关键帧值
            mykeys = (
                cmds.keyframe(
                    "{0}.{1}".format(selectedobj, a),
                    sl=True,
                    query=True,
                    valueChange=True,
                    absolute=True,
                )
                or []
            )
            # 检查是否至少有 3 个关键帧
            if len(mykeys) >= 3:
                index = 1
                # 遍历每个关键帧
                while index < len(mykeys) - 1:
                    # 获取当前关键帧的时间
                    time = cmds.keyframe(
                        "{0}.{1}".format(selectedobj, a),
                        sl=True,
                        timeChange=True,
                        query=True,
                    )[index]
                    # 获取前一个、当前和下一个关键帧的值
                    pre_value = mykeys[index - 1]
                    cur_value = mykeys[index]
                    nex_value = mykeys[index + 1]
                    # 计算三个关键帧的平均值
                    average = (pre_value + cur_value + nex_value) / 3
                    # 使用平均值和给定的百分比缩放当前关键帧的值
                    cmds.scaleKey(
                        "{0}.{1}".format(selectedobj, a),
                        time=(time, time),
                        valuePivot=average,
                        valueScale=perscentage,
                    )
                    # 将当前关键帧的切线类型设置为 "auto"
                    cmds.keyTangent(itt="auto", ott="auto")
                    index = index + 1
