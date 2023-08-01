# -*- coding: utf-8 -*-
"""
@FileName      : anim_curve_filter.py
@DateTime      : 2023/07/27 17:01:26
@Author        : Tian Chao
@Contact       : tianchao0533@163.com
@Software      : Maya 2023.3
@PythonVersion : python 3.9.7

灵感来源：
    动画曲线编辑辅助工具 - JAY JMS的文章 - 知乎
    https://zhuanlan.zhihu.com/p/35690523
    帖子中提供的脚本为加密文件，无法看到源代码，并且不支持Python3，在maya2022+版本无法使用，顾根据其解释的算法重新编写。
    该脚本用Pymel模块编写，请确保maya已安装Pymel模块。

过滤器算法：
    Dampen:
        在保持曲线连续性的情况下, 对曲线上选择的点增加或减少曲线的振幅. 实际用途即是对动画运动幅度的修改. 也可以同时选择多条曲线一起使用.
        其原理是：将首尾两帧连线,找出曲线上每一帧投射到连线上的值, 已此值作为pivot来对对应的曲线上的点进行拉伸或挤压.

    Butterworth:
        即 motionbuilder 里面的曲线过滤器butterworth. 在最大限度保持曲线细节的情况下, 对曲线进行一些光滑. 这个对于修改动态捕捉特别有用, 能够去掉一些捕捉不精准儿造成的抖动.
        其原理是：对曲线上每相邻的三帧, 求出他们的平均值, 以此平均值作为pivot来对第二帧对应曲线上的点进行拉伸或挤压.

    Smooth:
        即忽略最大限度的保持曲线细节, 对曲线进行大幅度的光滑. 需谨慎使用,因为会过滤掉很多动画细节.
        其原理和butterworth类似：对曲线上每相邻的三帧, 求出他们的平均值, 以此平均值直接赋予第二帧的数值.

    Twinner:
        和网上已有的免费工具 Twinning machine 类似. 对于手K动画很有用的添加中间帧的工具, 只需要选择控制器(可以多选), 拖动滑条能自动的K帧并且选择让这一帧的数值更偏向前一帧或者后一帧.
        其原理是：找到当前帧数相邻的前一个Key和后一个Key, 算出数值差, 然后做百分比运算.add()
使用方法：
    1.将此文件放入maya环境变量下路径中，一般为"\\Documents\\maya\\20xx\\scripts"
    2.在maya中执行 curve_filter = AnimCurveFilter();curve_filter.create_ui()
"""

from functools import partial
import pymel.core as pm


class AnimCurveFilter:
    """定义动画曲线过滤器类"""

    def __init__(self):
        """构造方法"""
        self.filter_radioCol = None
        self.value_slider = None
        self.default_value = 0
        self.keyframe_data = {}

    def create_ui(self):
        """创建UI"""
        try:
            pm.deleteUI("FilterCurve")
        except Exception as exc:
            print(exc)

        main_window = pm.window("FilterCurve", title="Curve filter")
        pm.columnLayout()
        # 创建radioButton选择器
        self.filter_radioCol = pm.radioCollection()
        rb_grp1 = pm.radioButtonGrp(
            numberOfRadioButtons=3,
            label="filters: ",
            labelArray3=["butterworth", "Dampen", "Smooth"],
            # 选择不同的按钮时，执行不同的命令，这里使用partial方法来传参，也可使用lambda方法来传参。
            changeCommand1=partial(self.switch_filter, 0),
            changeCommand2=partial(self.switch_filter, 1),
            changeCommand3=partial(self.switch_filter, 2),
            # changeCommand1=lambda *args: self.switch_filter(0),
            # 默认按钮为第0个
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
        # 创建浮点滑条按钮组件
        self.value_slider = pm.floatSliderButtonGrp(
            label="Value: ",
            field=True,
            # 指定拖动滑条命令，每次滑条拖动完毕执行的命令
            dragCommand=self.butterworth_filter,
            # 指定滑条值改变命令，每次滑条值改变所执行的命令。
            changeCommand=self.reset_slider,
            buttonLabel="reverse",
            # 指定按钮命令
            buttonCommand=self.anim_curve_reverse,
            # 设置滑条最大值最小值和默认值
            minValue=0.0,
            maxValue=100.0,
            fieldMinValue=0.0,
            fieldMaxValue=100.0,
            value=0.0,
        )
        pm.text(label="Butterworth:    在最大限度保持曲线细节的情况下, 对曲线进行一些光滑.", align='center')
        pm.text(label="Dampen:    在保持曲线连续性的情况下, 对曲线上选择的点增加或减少曲线的振幅.", align='center')
        pm.text(label="Smooth:    忽略最大限度的保持曲线细节, 对曲线进行大幅度的光滑. 需谨慎使用.", align='center')
        pm.text(label="simplify:    对动画曲线进行简化，减少关键帧.", align='center')
        pm.text(label="Twinner:    根据前后帧的值按照比例插值添加中间帧。", align='center')

        pm.showWindow(main_window)

    def switch_filter(self, filter_type: int, *args):
        """
        切换过滤器函数，根据过滤器类型切换过滤器

        Args:
            filter_type (int): 过滤器类型
        """
        # butterworth过滤器
        if filter_type == 0:
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
        # dampon过滤器
        elif filter_type == 1:
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
        # smooth过滤器
        elif filter_type == 2:
            self.default_value = 0
            pm.floatSliderButtonGrp(
                self.value_slider,
                edit=True,
                dragCommand=self.smooth_filter,
                changeCommand=self.reset_slider,
                buttonCommand=self.anim_curve_reverse,
                precision=0,
                step=1.0,
                fieldStep=1.0,
                sliderStep=1.0,
                minValue=1,
                maxValue=5,
                fieldMinValue=1,
                fieldMaxValue=5,
                value=1,
            )
        # simplify过滤器
        elif filter_type == 3:
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
        # twinner过滤器
        elif filter_type == 4:
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

    @staticmethod
    def get_keyframe_data(*args):
        """获取所选对象的关键帧数据。
        根据所选的对象列出他们的关键帧属性名称。关键帧时间点。关键帧数值。

        Returns:
            attr_list (list): 关键帧属性名称列表。
            time_value_list (list): 关键帧时间点的列表。
            key_value_list (list): 关键帧数值的列表。
        """
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
                        attr, sl=True, query=True, timeChange=True, absolute=True
                    )
                    time_value_list.append(time_value)

        return attr_list, time_value_list, key_value_list

    def butterworth_filter(self, *args):
        """给给定的关键帧动画应用Butterworth过滤器。

        即 motionbuilder 里面的曲线过滤器butterworth.
        在最大限度保持曲线细节的情况下, 对曲线进行一些光滑.
        这个对于修改动态捕捉特别有用, 能够去掉一些捕捉不精准儿造成的抖动.

        其原理是：对曲线上每相邻的三帧, 求出他们的平均值, 以此平均值作为pivot来对第二帧对应曲线上的点进行拉伸或挤压.
        """

        # 获取滑条数据并重新插值计算。
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 1.0, -2.0, filter_value)
        # 关闭缓存曲线更新，以便后面返回原始曲线数据。
        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i, attr in enumerate(attr_list):
            time_value = time_value_list[i]
            key_value = key_value_list[i]

            if len(key_value) >= 3:
                for j in range(1, len(key_value) - 1):
                    pre_value = key_value[j - 1]
                    cur_value = key_value[j]
                    nex_value = key_value[j + 1]
                    # 求出相邻三帧的平均值
                    average_value = (pre_value + cur_value + nex_value) / 3
                    # 以此平均值作为轴心来对第二帧对应曲线上的点进行拉伸或挤压.
                    pm.scaleKey(
                        attr,
                        time=(time_value[j], time_value[j]),
                        valuePivot=average_value,
                        valueScale=scale_value,
                    )
                    # 调整曲线切线为自动
                    pm.keyTangent(itt="auto", ott="auto")

    def dampon_filter(self, *args):
        """给给定的关键帧动画应用dampon过滤器

        在保持曲线连续性的情况下, 对曲线上选择的点增加或减少曲线的振幅.
        实际用途即是对动画运动幅度的修改. 也可以同时选择多条曲线一起使用.

        其原理是：将首尾两帧连线,找出曲线上每一帧投射到连线上的值, 已此值作为pivot来对对应的曲线上的点进行拉伸或挤压.
        """

        # 获取滑条数据并重新插值计算。
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 0.5, 1.5, filter_value)
        # 关闭缓存曲线更新，以便后面返回原始曲线数据。
        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i, attr in enumerate(attr_list):
            time_value = time_value_list[i]
            key_value = key_value_list[i]

            if len(key_value) >= 2 and len(time_value) >= 2:
                # 获取整条曲线的切线，即整条曲线的首末帧的 值差 和 时间差 之比。
                tangent = (key_value[-1] - key_value[0]) / abs(
                    time_value[-1] - time_value[0]
                )
                for j in range(1, len(time_value) - 1):
                    # 根据切线和时间差计算缩放中心点
                    # 切线乘以时间差可以得到从第一个关键帧到当前关键帧的属性值变化量，然后再加上第一个关键帧的属性值，就可以得到当前关键帧的缩放中心点位置。
                    scale_pivot = (
                        tangent * (time_value[j] - time_value[0]) + key_value[0]
                    )
                    # 使用缩放中心点和百分比缩放关键帧
                    pm.scaleKey(
                        attr,
                        time=(time_value[j], time_value[j]),
                        valuePivot=scale_pivot,
                        valueScale=scale_value,
                    )
        """
        关键帧之间的切线表示属性值的变化率。计算切线是为了确定在关键帧之间进行缩放时，属性值的变化率。

        算法的步骤如下：

        1.获取关键帧的值变化列表 key_value 和时间变化列表 time_value
        2.计算切线 tangent，使用公式 tangent = (key_value[-1] - key_value[0]) / abs(time_value[-1] - time_value[0])。
        这个公式计算的是第一个关键帧和最后一个关键帧之间的平均变化率，即切线。
        3.遍历每个关键帧，通过以下步骤计算缩放中心点的位置：
        4.获取当前关键帧的时间 time。
        5.计算时间差 time_value[i] - time_value[0]，表示当前关键帧相对于第一个关键帧的时间差。
        6.将时间差乘以切线 tangent，得到从第一个关键帧到当前关键帧的属性值变化量。
        7.将属性值变化量加上第一个关键帧的属性值 key_value[0]，得到当前关键帧的缩放中心点位置。

        通过这个算法，可以根据关键帧之间的切线和时间差，计算出在关键帧之间进行缩放时的缩放中心点的位置。这样可以实现对关键帧进行精确的缩放操作。
        """

    def smooth_filter(self, *args):
        """给给定的关键帧动画应用smooth过滤器
        忽略最大限度的保持曲线细节, 对曲线进行大幅度的光滑. 需谨慎使用,因为会过滤掉很多动画细节.
        其原理和butterworth类似：对曲线上每相邻的三帧, 求出他们的平均值, 以此平均值直接赋予第二帧的数值.
        UI滑条值为执行平滑脚本次数。
        """
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for i, attr in enumerate(attr_list):
            time_value = time_value_list[i]
            key_value = key_value_list[i]
            if len(key_value) >= 3:
                for j in range(1, len(key_value) - 1):
                    pre_value = key_value[j - 1]
                    cur_value = key_value[j]
                    nex_value = key_value[j + 1]

                    average_value = (pre_value + cur_value + nex_value) / 3

                    pm.keyframe(
                        attr,
                        time=(time_value[j], time_value[j]),
                        valueChange=average_value,
                    )
        try:
            for i in range(filter_value):
                self.smooth_filter()
        except TypeError:
            pass

    def simplify_filter(self, *args):
        """
        对给定的关键帧动画应用simplify过滤器, 简化所选对象属性的关键帧。

        Returns:
            None
        """
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 0.0, 3.0, filter_value)

        pm.bufferCurve(animation="keys", overwrite=False)

        attr_list, time_value_list, _ = self.get_keyframe_data()

        for i, attr in enumerate(attr_list):
            time_value = time_value_list[i]
            # 检查属性是否有关键帧
            if len(time_value) > 0:
                # 在给定的时间范围内简化属性的关键帧
                pm.simplify(
                    attr,
                    time=(time_value[0], time_value[-1]),
                    timeTolerance=scale_value,
                    floatTolerance=scale_value,
                    valueTolerance=scale_value,
                )
        # 简化完成后重选所选的关键帧，以便下次简化
        pm.selectKey(
            attr_list,
            replace=True,
            time=(time_value_list[0][0], time_value_list[0][-1]),
        )

    def twinner_filter(self, *args):
        """和Twinning machine工具类似.
        对于手K动画很有用的添加中间帧的工具, 只需要选择控制器(可以多选), 拖动滑条能自动的K帧并且选择让这一帧的数值更偏向前一帧或者后一帧.
        """
        filter_value = pm.floatSliderButtonGrp(self.value_slider, q=True, v=True)
        scale_value = self.remap(0.0, 100.0, 0, 1.0, filter_value)

        current_time = pm.currentTime(query=True)
        attr_list, time_value_list, key_value_list = self.get_keyframe_data()

        for attr in attr_list:
            current_value = pm.keyframe(attr, time=current_time, query=True, eval=True)
            if current_value:
                # 前一个关键帧的时间点
                pre_time = pm.findKeyframe(attr, time=current_time, which="previous")
                # 前一个关键帧的值。
                pre_value = pm.keyframe(attr, time=pre_time, query=True, eval=True)
                # 后一个关键帧的时间点。
                next_time = pm.findKeyframe(attr, time=current_time, which="next")
                # 后一个关键帧的值。
                next_value = pm.keyframe(attr, time=next_time, query=True, eval=True)
                # 如果前后两个关键帧同时存在，中间却没有关键帧，则新增一个关键帧
                if pre_value and next_value:
                    if not pm.keyframe(attr, time=current_time, query=True):
                        pm.setKeyframe(attr, time=current_time)
                    # 如果前一个关键帧的值不等于后一个关键帧的值。
                    if next_value[0] != pre_value[0]:
                        # 根据前一个关键帧和后一个关键帧的值，差值计算中间关键帧一个新值
                        # 算法为：后一个关键帧的值减去前一个关键帧的值，乘以比例，加上前一个关键帧的值
                        current_key_value = (
                            scale_value * (next_value[0] - pre_value[0]) + pre_value[0]
                        )
                        # 更新关键帧的值
                        pm.keyframe(
                            attr, time=current_time, valueChange=current_key_value
                        )

    @staticmethod
    def anim_curve_reverse(*args):
        """将动画曲线返回修改前的状态
        原理：利用maya曲线编辑器的缓存曲线（bufferCurve）
        """
        try:
            # 返回修改前缓存曲线的状态
            pm.bufferCurve(animation="keys", swap=True)
            # 覆盖缓存曲线为当前曲线
            pm.bufferCurve(animation="keys", overwrite=True)
        except Exception as exc:
            print(exc)

    def reset_slider(self, *args):
        """重设浮点滑条"""
        try:
            pm.floatSliderButtonGrp(
                self.value_slider, edit=True, value=self.default_value
            )
        except Exception as exc:
            print(exc)

    @staticmethod
    def remap(i_min, i_max, o_min, o_max, v):
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
