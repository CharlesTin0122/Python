import pymel.core as pm
import pymel.core.datatypes as dt


def joint_at_selected_vertexes():
    """This function calculates the center point of the selected vertexes
    and creates a joint at that position.

    Raises:
        RuntimeError: Target not selected
    """
    vertexes = pm.ls(sl=True, flatten=True)  # 获取所选顶点
    # 错误处理
    if not vertexes:
        raise RuntimeError("请至少选择一个顶点")

    vertexes_num = len(vertexes)  # 获取顶点个数
    # 计算中心点
    sum_pos = dt.Point([0, 0, 0])  # 创建零向量
    # 遍历所有顶点，求出所有顶点位置向量的和
    for vertex in vertexes:
        vertex_pos = vertex.getPosition(space="world")
        sum_pos += vertex_pos
    # 所有顶点位置向量的和除以顶点个数，求出中心点
    center_point = sum_pos / vertexes_num
    # 创建骨骼
    pm.select(clear=True)
    pm.joint(position=center_point)


joint_at_selected_vertexes()
