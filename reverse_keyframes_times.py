import pymel.core as pm
'''
这段代码使用了 pymel 库来对动画中的选定关键帧进行操作。
它计算选定的关键帧数量,并且如果数量大于0,则获取这些关键帧的时间、值和索引数组。
然后，它计算了这些关键帧值的最大值和最小值之间的中间值，并使用该中间值来对关键帧进行反向缩放。
'''
sel = pm.selected()
key_count = pm.keyframe(sel, selected=True, q=True, keyframeCount=True)

if key_count:

    selected_Curves = pm.keyframe(selected=True, q=True, name=True)
    for c in range(0, len(selected_Curves)):
        channel = selected_Curves[c]

        # Get indexex from time-aray
        time_array = pm.keyframe(channel, selected=False, q=True, timeChange=True)
        # Get selected times
        sel_time_array = pm.keyframe(channel, selected=True, q=True, timeChange=True)
        # Get values matching the sel time list
        value_array = pm.keyframe(channel, selected=True, q=True, valueChange=True)
        # Get indexes from selected keframes
        index_array = [n for n, x in enumerate(time_array) if x in sel_time_array]

        # Get middle value betweeen the highest and lowest value.
        # We use this value divided by 2 to get the mid-point and can use it in the scale
        mid_value = (sorted(value_array)[-1] + sorted(value_array)[0]) / 2

        for n, i in enumerate(index_array):
            pm.scaleKey(channel, index=[i], valuePivot=mid_value, valueScale=-1)
