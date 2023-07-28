# -*- coding: utf-8 -*-
"""
@FileName      : anim_curve_filter.py
@DateTime      : 2023/07/27 17:01:26
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7
"""

from functools import partial
import pymel.core as pm


class AnimCurveFilter:
    def __init__(self):
        self.filter_radioCol = None
        self.value_slider = None
        self.default_value = None
        self.keyframe_data = {}

    def create_ui(self):
        try:
            pm.deleteUI("FilterCurve")
        except Exception as exc:
            print(exc)

        main_window = pm.window("FilterCurve", title="Curve filter")
        pm.columnLayout()
        self.filter_radioCol = pm.radioCollection()
        rb_grp1 = pm.radioButtonGrp(
            numberOfRadioButtons=3,
            label="filters: ",
            labelArray3=["butterworth", "Dampen", "Smooth"],
            changeCommand1=partial(self.switch_filter, 0),
            changeCommand2=partial(self.switch_filter, 1),
            changeCommand3=partial(self.switch_filter, 2),
            select=0,
        )
        pm.radioButtonGrp(
            numberOfRadioButtons=2,
            shareCollection=rb_grp1,
            label="",
            labelArray2=["simplify", "Twinner"],
            changeCommand1=partial(self.switch_filter, 3),
            changeCommand2=partial(self.switch_filter, 4),
        )
        self.value_slider = pm.floatSliderButtonGrp(
            label="Value: ",
            field=True,
            dragCommand=self.butterworth_filter,
            changeCommand=self.reset_slider,
            buttonLabel="reverse",
            buttonCommand=self.anim_curve_reverse,
            minValue=0.0,
            maxValue=100.0,
            fieldMinValue=0.0,
            fieldMaxValue=100.0,
            value=0.0,
        )

        pm.showWindow(main_window)

    def switch_filter(self, filter: int, *args):
        if filter == 0:
            self.default_value = 0
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.butterworth_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                minValue=0.0,
                maxValue=100.0,
                fieldMinValue=0.0,
                fieldMaxValue=100.0,
                value=0.0,
            )
        elif filter == 1:
            self.default_value = 50
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.dampon_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                minValue=0.0,
                maxValue=100.0,
                fieldMinValue=0.0,
                fieldMaxValue=100.0,
                value=50.0,
            )
        elif filter == 2:
            self.default_value = 0
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.smooth_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                minValue=0.0,
                maxValue=100.0,
                fieldMinValue=0.0,
                fieldMaxValue=100.0,
                value=0.0,
            )
        elif filter == 3:
            self.default_value = 0
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.simplify_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                minValue=0.0,
                maxValue=100.0,
                fieldMinValue=0.0,
                fieldMaxValue=100.0,
                value=0.0,
            )
        elif filter == 4:
            self.default_value = 50.0
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.twinner_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                minValue=0.0,
                maxValue=100.0,
                fieldMinValue=0.0,
                fieldMaxValue=100.0,
                value=50.0,
            )

    def get_keyframe_data(self, *args):
        key_value_list = []
        time_value_list = []
        attr_list = []

        sel_obj_list = pm.selected()
        if sel_obj_list:
            for obj in sel_obj_list:
                attrs = pm.listAnimatable(obj)
                attr_list.extend(attrs)
                for attr in attrs:
                    key_value = pm.keyframe(
                        attr,
                        sl=True,
                        query=True,
                        valueChange=True,
                        absolute=True,
                    )
                    key_value_list.append(key_value)

                    time_value = pm.keyframe(
                        attr,
                        sl=True,
                        query=True,
                        timeChange=True,
                        absolute=True
                    )
                    time_value_list.append(time_value)

        return attr_list, time_value_list, key_value_list

    def butterworth_filter(self, *args):
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 1.0, -2.0, filter_value)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i in range(1, len(attr_list) - 1):
            attr = attr_list[i]
            time_value = time_value_list[i]
            key_value = key_value_list[i]

            if len(key_value) >= 3:
                pre_value = key_value[i - 1]
                cur_value = key_value[i]
                nex_value = key_value[i + 1]

                average_value = (pre_value + cur_value + nex_value) / 3

                pm.scaleKey(
                    attr,
                    time=(time_value, time_value),
                    valuePivot=average_value,
                    valueScale=scale_value,
                )
                pm.keyTangent(itt="auto", ott="auto")

    def dampon_filter(self, *args):
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 0.0, 2.0, filter_value)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i in range(1, len(attr_list) - 1):
            attr = attr_list[i]
            time_value = time_value_list[i]
            key_value = key_value_list[i]

            if len(key_value) >= 2 and len(time_value) >= 2:
                tangent = (key_value[-1] - key_value[0]) / abs(
                    time_value[-1] - time_value[0]
                )
                for key_time in time_value:
                    scale_pivot = tangent * (key_time - time_value[0]) + key_value[0]
                    pm.scaleKey(
                        attr,
                        time=(key_time, key_time),
                        valuePivot=scale_pivot,
                        valueScale=scale_value,
                    )

    def smooth_filter(self, *args):
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 1.0, 5.0, filter_value)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i in range(1, len(attr_list) - 1):
            attr = attr_list[i]
            time_value = time_value_list[i]
            key_value = key_value_list[i]
            if len(key_value) >= 3:
                pre_value = key_value[i - 1]
                cur_value = key_value[i]
                nex_value = key_value[i + 1]

                average_value = (pre_value + cur_value + nex_value) / 3

                pm.keyframe(
                    attr,
                    time=(time_value, time_value),
                    valueChange=average_value * scale_value,
                )

    def simplify_filter(self, *args):
        """
        根据给定的百分比容差简化所选对象属性的关键帧。

        Args:
            percentage (float): 关键帧简化的容差百分比。

        Returns:
            None
        """
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 1.0, 0.0, filter_value)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i in range(1, len(attr_list) - 1):
            attr = attr_list[i]
            time_value = time_value_list[i]

            # 检查属性是否有关键帧
            if len(time_value) > 0:
                # 获取关键帧的起始时间和结束时间
                time_start = time_value[0]
                time_end = time_value[-1]
                # 在给定的时间范围内简化属性的关键帧
                pm.simplify(
                    attr,
                    time=(time_start, time_end),
                    timeTolerance=scale_value,
                    floatTolerance=scale_value,
                    valueTolerance=scale_value,
                )
                # 选择简化后的关键帧
                pm.selectKey(attr, time=(time_start, time_end))

    def twinner_filter(self, *args):
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 0, 1.0, filter_value)

        current_time = pm.currentTime(query=True)
        attr_list, time_value_list, key_value_list = self.get_keyframe_data()
        for i in range(1, len(attr_list) - 1):
            attr = attr_list[i]

            current_value = pm.keyframe(attr, time=current_time, query=True, eval=True)
            if current_value:
                pre_time = pm.findKeyframe(attr, time=current_time, which="previous")
                pre_value = pm.keyframe(attr, time=pre_time, query=True, eval=True)
                next_time = pm.findKeyframe(attr, time=current_time, which="next")
                next_value = pm.keyframe(attr, time=next_time, query=True, eval=True)
                if pre_value and next_value:
                    if not pm.keyframe(attr, time=current_time, query=True):
                        pm.setKeyframe(attr, time=current_time)
                    if next_value[0] != pre_value:
                        current_key_value = (
                            scale_value * (next_value[0] - pre_value[0]) + pre_value[0]
                        )
                        pm.keyframe(
                            attr, time=current_time, valueChange=current_key_value
                        )

    def anim_curve_reverse(self, *args):
        try:
            pm.bufferCurve(animation="keys", swap=True)
            pm.bufferCurve(animation="keys", overwrite=True)
        except Exception as exc:
            print(exc)

    def reset_slider(self, *args):
        try:
            pm.floatSliderButtonGrp(
                self.value_slider, edit=True, value=self.default_value
            )
        except Exception as exc:
            print(exc)

    def remap(self, i_min, i_max, o_min, o_max, v):
        """
        将一个线性比例尺上的值重新映射到另一个线性比例尺上，结合了线性插值和反线性插值。

        Args:
            i_min (float): 输入比例尺的最小值。
            i_max (float): 输入比例尺的最大值。
            o_min (float): 输出比例尺的最小值。
            o_max (float): 输出比例尺的最大值。
            v (float): 需要重新映射的值。

        Returns:
            float: 重新映射后的值。

        Examples:
            45 == remap(0, 100, 40, 50, 50)
            6.2 == remap(1, 5, 3, 7, 4.2)
        """
        return (1 - (v - i_min) / (i_max - i_min)) * o_min + (v - i_min) / (
            i_max - i_min
        ) * o_max


if __name__ == "__main__":
    curve_filter = AnimCurveFilter()
    curve_filter.create_ui()
