import ast
import maya.cmds as cmds


def return_attribute():
    attr_list = []
    curves = cmds.animCurveEditor('graphEditor1GraphEd', curvesShown=True, q=True)
    for i in curves:
        if cmds.keyframe(i.replace('_', '_'), sl=True, query=True, timeChange=True):
            attr_list.append(i.replace('_', '_'))

    return attr_list


def get_mytimes(attr):
    mytimes = cmds.keyframe(attr, sl=True, query=True, timeChange=True) or []
    if len(mytimes) > 0:
        for x in range(int(mytimes[0]), int(mytimes[-1])):
            if cmds.keyframe(attr, time=(x, x), valueChange=True, q=True):
                if x not in mytimes:
                    mytimes.append(x)

    return mytimes


def get_mykeys(attr):
    mykeys = cmds.keyframe(attr, sl=True, query=True, valueChange=True, absolute=True) or []
    return mykeys


def get_dict(attr):
    dic = {}
    mykeys = get_mykeys(attr) or []
    if len(mykeys) >= 3:
        index = 1
        while index < len(mykeys) - 1:
            time = get_mytimes(attr)[index]
            cur_value = mykeys[index]
            dic[time] = cur_value
            index = index + 1

    cmds.optionVar(sv=('mydict_{0}'.format(attr), str(dic)))
    return dic


def resample_keys(kv, thresh):
    if kv.keys():
        start = float(min(kv.keys()))
        end = float(max(kv.keys()))
        start_value = float(kv[start])
        end_value = float(kv[end])
        total_error = 0
        offender = -1
        outlier = -1
        for k, v in kv.items():
            if end - start != 0:
                time_ratio = (k - start) / (end - start)
                sample = time_ratio * end_value + (1 - time_ratio) * start_value
                delta = abs(v - sample)
                total_error += delta
                if delta > outlier:
                    outlier = delta
                    offender = k

        if total_error < thresh or len(kv.keys()) == 2:
            return [{start: start_value,
                     end: end_value}]
        else:
            s1 = {kk: vv for kk, vv in kv.items() if kk <= offender}
            s2 = {kk: vv for kk, vv in kv.items() if kk >= offender}
            return resample_keys(s1, thresh) + resample_keys(s2, thresh)


def rejoin_keys(kvs):
    result = {}
    for item in kvs:
        result.update(item)

    return result


def decimate(attr, tolerance):
    mydict = ast.literal_eval(cmds.optionVar(q='mydict_{0}'.format(attr)))
    return rejoin_keys(resample_keys(mydict, tolerance))


def resample(attr, tolerance, mytimes):
    mytimes = get_mytimes(attr)
    mytimes.sort()
    resample_dict = decimate(attr, tolerance)
    newtimes = resample_dict.keys()
    newtimes.sort()
    mytimes.pop(0)
    mytimes.pop(-1)
    if len(mytimes) > len(newtimes):
        for t in [i for i in mytimes + newtimes if i not in mytimes or i not in newtimes]:
            cmds.cutKey(attr, time=(t, t), option='keys')

    elif len(mytimes) < len(newtimes):
        for x in [i for i in mytimes + newtimes if i not in mytimes or i not in newtimes]:
            cmds.setKeyframe(attr, t=x)
            cmds.keyframe(attr, time=(x, x), valueChange=resample_dict[x])


def record():
    for attr in return_attribute():
        mytimes = get_mytimes(attr)
        if len(mytimes) > 0:
            get_dict(attr)


def resampleDrag(value, tolerance_value):
    for attr in return_attribute():
        mytimes = get_mytimes(attr)
        if len(mytimes) > 0:
            resample(attr, value / float(tolerance_value), mytimes)


def pre_key(i, a):
    current_time = cmds.currentTime(query=True)
    previous_time = cmds.findKeyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), which='previous')
    previous_key = cmds.keyframe('{0}.{1}'.format(i, a), time=(previous_time, previous_time), query=True, eval=True)
    return previous_key


def next_key(i, a):
    current_time = cmds.currentTime(query=True)
    next_time = cmds.findKeyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), which='next')
    next_key = cmds.keyframe('{0}.{1}'.format(i, a), time=(next_time, next_time), query=True, eval=True)
    return next_key


def pre_key_time(i, a):
    current_time = cmds.currentTime(query=True)
    previous_time = cmds.findKeyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), which='previous')
    return previous_time


def next_key_time(i, a):
    current_time = cmds.currentTime(query=True)
    next_time = cmds.findKeyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), which='next')
    return next_time


def twinner(value):
    current_time = cmds.currentTime(query=True)
    list = cmds.ls(selection=True)
    for i in list:
        attr = cmds.listAttr(i, keyable=True)
        for a in attr:
            if cmds.objExists('{0}.{1}'.format(i, a)):
                current_value = cmds.keyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), query=True,
                                              eval=True)
                if current_value:
                    pre_value = pre_key(i, a)
                    next_value = next_key(i, a)
                    if pre_value and next_value:
                        if not cmds.keyframe('{0}.{1}'.format(i, a), time=(current_time, current_time), q=True):
                            cmds.setKeyframe('{0}.{1}'.format(i, a), t=current_time)
                        if next_value[0] != current_value:
                            key_value = value / 100.0 * (next_value[0] - pre_value[0]) + pre_value[0]
                            cmds.keyframe('{0}.{1}'.format(i, a), time=(current_time, current_time),
                                          valueChange=key_value)


def scalekey(perscentage):
    selectedobjList = cmds.ls(sl=True)
    for selectedobj in selectedobjList:
        Attr = cmds.listAttr(selectedobj, keyable=True)
        for a in Attr:
            mykeys = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, query=True, valueChange=True,
                                   absolute=True) or []
            timechange = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, query=True, timeChange=True,
                                       absolute=True) or []
            if len(mykeys) >= 2 and len(timechange) >= 2:
                tangent = (mykeys[-1] - mykeys[0]) / abs(timechange[-1] - timechange[0])
                index = 1
                while index < len(mykeys) - 1:
                    time = cmds.keyframe('{0}.{1}'.format(selectedobj, a), selected=True, query=True, timeChange=True)[
                        index]
                    scalePivot = tangent * (time - timechange[0]) + mykeys[0]
                    cmds.scaleKey('{0}.{1}'.format(selectedobj, a), time=(time, time), valuePivot=scalePivot,
                                  valueScale=perscentage)
                    index = index + 1


def smooth():
    selectedobjList = cmds.ls(sl=True)
    for selectedobj in selectedobjList:
        Attr = cmds.listAttr(selectedobj, keyable=True)
        for a in Attr:
            mykeys = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, query=True, valueChange=True,
                                   absolute=True) or []
            if len(mykeys) >= 3:
                index = 1
                while index < len(mykeys) - 1:
                    time = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, timeChange=True, query=True)[index]
                    pre_value = mykeys[index - 1]
                    cur_value = mykeys[index]
                    nex_value = mykeys[index + 1]
                    average = (pre_value + cur_value + nex_value) / 3
                    cmds.keyframe('{0}.{1}'.format(selectedobj, a), time=(time, time), valueChange=average)
                    index = index + 1


def simplify_(perscentage):
    value = perscentage / 100.0
    selectedobjList = cmds.ls(sl=True)
    for selectedobj in selectedobjList:
        Attr = cmds.listAttr(selectedobj, keyable=True)
        for a in Attr:
            mytimes = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, query=True, timeChange=True,
                                    absolute=True) or []
            if len(mytimes) > 0:
                time_s = mytimes[0]
                time_e = mytimes[-1]
                print(time_s)
                print(time_e)
                cmds.simplify('{0}.{1}'.format(selectedobj, a), time=(time_s, time_e), timeTolerance=value,
                              floatTolerance=value, valueTolerance=value)
                cmds.selectKey('{0}.{1}'.format(selectedobj, a), time=(time_s, time_e))


def butterworth(perscentage):
    selectedobjList = cmds.ls(sl=True)
    for selectedobj in selectedobjList:
        Attr = cmds.listAttr(selectedobj, keyable=True)
        for a in Attr:
            mykeys = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, query=True, valueChange=True,
                                   absolute=True) or []
            if len(mykeys) >= 3:
                index = 1
                while index < len(mykeys) - 1:
                    time = cmds.keyframe('{0}.{1}'.format(selectedobj, a), sl=True, timeChange=True, query=True)[index]
                    pre_value = mykeys[index - 1]
                    cur_value = mykeys[index]
                    nex_value = mykeys[index + 1]
                    average = (pre_value + cur_value + nex_value) / 3
                    cmds.scaleKey('{0}.{1}'.format(selectedobj, a), time=(time, time), valuePivot=average,
                                  valueScale=perscentage)
                    cmds.keyTangent(itt='auto', ott='auto')
                    index = index + 1
