import pymel.core as pm


def get_mirrored_name(obj_name, naming_pairs=None):
    """
    根据命名约定生成镜像对象的名称。

    Args:
        obj_name (str): 原始对象名称
        naming_pairs (list of tuples): 命名对，例如 [('_L', '_R'), ('left', 'right')]

    Returns:
        str or None: 镜像对象名称，如果无法生成则返回 None
    """
    if naming_pairs is None:
        naming_pairs = [
            ("_L", "_R"),
            ("_R", "_L"),
            ("left", "right"),
            ("right", "left"),
        ]

    for source, target in naming_pairs:
        if source in obj_name:
            mirrored_name = obj_name.replace(source, target)
            return mirrored_name

    return None


def mirror_selection(naming_pairs=None, clear_if_none=True, verbose=True):
    """
    镜像选择对象：将包含特定命名（如 _L）的对象替换为对应命名（如 _R）的对象。

    Args:
        naming_pairs (list of tuples): 命名对，例如 [('_L', '_R'), ('left', 'right')]
        clear_if_none (bool): 如果没有镜像对象，是否清空选择
        verbose (bool): 是否打印详细的警告和信息

    Returns:
        list: 成功选择的镜像对象列表
    """
    # 获取当前选择
    selected = pm.selected()

    if not selected:
        if verbose:
            pm.warning("没有选择任何对象！")
        if clear_if_none:
            pm.select(clear=True)
        return []

    # 用于存储镜像对象
    mirrored_objects = []
    failed_objects = []

    for obj in selected:
        obj_name = obj.name()
        mirrored_name = get_mirrored_name(obj_name, naming_pairs)

        if not mirrored_name:
            failed_objects.append(obj_name)
            continue

        # 检查镜像对象是否存在
        if pm.objExists(mirrored_name):
            mirrored_objects.append(pm.PyNode(mirrored_name))
        else:
            failed_objects.append(obj_name)
            if verbose:
                pm.warning(f"镜像对象 {mirrored_name} 不存在")

    # 选择镜像对象
    if mirrored_objects:
        pm.select(mirrored_objects, replace=True)
    elif clear_if_none:
        pm.select(clear=True)

    # 打印总结信息
    if verbose and failed_objects:
        pm.warning(f"以下对象无法镜像选择: {', '.join(failed_objects)}")

    return mirrored_objects


# 示例用法
if __name__ == "__main__":
    # 默认命名对
    default_naming_pairs = [
        ("_L", "_R"),
        ("_R", "_L"),
        ("left", "right"),
        ("right", "left"),
    ]
    mirror_selection(
        naming_pairs=default_naming_pairs, clear_if_none=True, verbose=True
    )
