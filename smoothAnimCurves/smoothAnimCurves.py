import pymel.core as pm


def smoothAnimCurve():
    """
    平滑动画曲线，通过对每个关键帧与相邻关键帧的值进行平均处理。
    用于对动画曲线进行平滑处理。它会遍历每一个动画曲线，检查是否至少有3个关键帧，然后创建一个曲线的副本。
    它计算每个关键帧的平均值，并将其赋值给副本曲线。最后，它将副本曲线的值重新赋值给原始曲线，并删除副本曲线。
    """
    # 获取动画曲线
    AnimCurve = pm.keyframe(q=True, n=True)
    # 遍历每个曲线
    for cv in AnimCurve:
        # 获取选中的关键帧
        keys = pm.keyframe(cv, q=True, sl=True)
        sizeOfKeys = len(keys)
        # 如果选中的关键帧少于3个，则跳过该曲线
        if sizeOfKeys < 3:
            continue
        # 复制曲线
        dupCurve = pm.duplicate(cv)
        # 遍历每个关键帧（排除第一个和最后一个）
        for i in range(1, sizeOfKeys - 1):
            # 获取前一个、当前和后一个关键帧的值
            preVal = pm.keyframe(cv, time=(keys[i - 1], keys[i - 1]), q=True, vc=True)
            curVal = pm.keyframe(cv, time=(keys[i], keys[i]), q=True, vc=True)
            nexVal = pm.keyframe(cv, time=(keys[i + 1], keys[i + 1]), q=True, vc=True)
            # 计算平均值
            aveVal = (preVal[0] + curVal[0] + nexVal[0]) / 3
            # 将平均值设置为当前关键帧的复制曲线的值
            pm.keyframe(dupCurve, time=(keys[i], keys[i]), a=True, vc=aveVal)
        # 将复制曲线的值复制回原始曲线
        for i in range(1, sizeOfKeys - 1):
            dupCurVal = pm.keyframe(dupCurve, time=(keys[i], keys[i]), q=True, vc=True)
            pm.keyframe(cv, time=(keys[i], keys[i]), a=1, vc=dupCurVal[0])
        # 删除复制曲线
        pm.delete(dupCurve[0])
