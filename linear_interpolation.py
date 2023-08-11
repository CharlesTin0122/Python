# -*- coding: utf-8 -*-
"""
@FileName : linear_interpolation.py
@DateTime : 2023/07/27 13:55:23
@Author   : Tian Chao
@Contact  : tianchao0533@163.com
"""


def lerp(a: float, b: float, t: float) -> float:
    """
    在给定的范围 a 到 b 上进行线性插值，使用 t 作为该范围上的插值点。

    Parameters:
    a (float): 起始值.
    b (float): 结束值.
    t (float): 差值因子.

    Returns:
    float: 插值.

    Examples

        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b


def inv_lerp(a: float, b: float, v: float) -> float:
    """
    逆线性插值，获取 v 所在的 a 和 b 之间的分数。

    Parameters
    ----------
    a : float
        范围的下限。
    b : float
        范围的上限。
    v : float
        要计算分数的值。

    Returns：
    float：“v”所在的“a”到“b”之间的分数

    Examples
    --------
    0.5 == inv_lerp(0, 100, 50)
    0.8 == inv_lerp(1, 5, 4.2)
    """
    return (v - a) / (b - a)


def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
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
    return lerp(o_min, o_max, inv_lerp(i_min, i_max, v))
    # return (1 - (v - i_min) / (i_max - i_min)) * o_min + (v - i_min) / (i_max - i_min) * o_max
