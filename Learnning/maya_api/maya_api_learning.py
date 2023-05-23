import maya.OpenMaya as OpenMaya


# 获取选择的物体名称
def get_selected():
    # 创建物体列表,是一个空列表
    sel = OpenMaya.MSelectionList()
    # 获取选择物体并传入sel列表
    OpenMaya.MGlobal.getActiveSelectionList(sel)
    # 遍历sel列表
    for i in range(sel.length()):
        # 创建物体路径列表，MDagPath：物体的路径（物体的层级和父子关系）
        dag_path = OpenMaya.MDagPath()
        # 利用MSelectionList类的getDagPath方法将物体传入dag_path列表,有两个参数，第一个是对象的索引,第二个是MDagPath类的实例
        sel.getDagPath(i, dag_path)
        # 打印dag_path列表每项的长名称
        print(dag_path.fullPathName())


get_selected()


# 通过名称列表选择物体
def selected_by_name(name_list):
    # 创建物体列表
    sel = OpenMaya.MSelectionList()
    # 遍历提供的名称列表
    for name in name_list:
        # 将名称添加到物体列表
        sel.add(name)
    # 设置物体列表到选择列表
    OpenMaya.MGlobal.setActiveSelectionList(sel)


selected_by_name(['pCube2', 'pSphere1'])


# 通过遍历maya场景中的所有物体来筛选我们想要的物体
def is_all():
    # OpenMaya.MItDag用于在场景中遍历和操作 DAG（Directed Acyclic Graph）层次结构。
    """遍历类型（Traversal Type）：指定遍历 DAG 的方式。常用的遍历类型包括：

    OpenMaya.MItDag.kDepthFirst：深度优先遍历。
    OpenMaya.MItDag.kBreadthFirst：广度优先遍历。
    OpenMaya.MItDag.kDepthFirstUp：从叶子节点开始的反向深度优先遍历。
    OpenMaya.MItDag.kBreadthFirstUp：从叶子节点开始的反向广度优先遍历。
    过滤类型（Filter Type）：指定遍历的节点类型。常用的过滤类型通过 OpenMaya.MFn 类中的常量来表示，例如：

    OpenMaya.MFn.kInvalid：遍历所有类型的节点。
    OpenMaya.MFn.kCamera：只遍历相机节点。
    OpenMaya.MFn.kMesh：只遍历网格节点。
    OpenMaya.MFn.kJoint：只遍历关节节点，等等。"""
    mit_dag = OpenMaya.MItDag(OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kInvalid)
    while not mit_dag.isDone():
        item = mit_dag.currentItem()  # 迭代器当前对象，
        # MFnDagNode类用于操作和查询 DAG（Directed Acyclic Graph）节点的属性和功能
        fn_dag_node = OpenMaya.MFnDagNode(item)
        print(fn_dag_node.typeName())  # 查询类型
        print(fn_dag_node.fullPathName())  # 长名称
        print(fn_dag_node.name())  # 名称
        mit_dag.next()  # 继续迭代


is_all()


# 获取父子对象
def find_hierarchy():
    selected = OpenMaya.MSelectionList()  # 创建对象列表实例
    OpenMaya.MGlobal.getActiveSelectionList(selected)  # 获取选择的对象装入对象列表

    sel_dag_path = OpenMaya.MDagPath()  # 创建MDagPath实例
    selected.getDagPath(0, sel_dag_path)  # 将选择列表对象的第0个装入MDagPath实例

    sel_dag_path_fn = OpenMaya.MFnDagNode(sel_dag_path)  # 创建DagNode函数集，将sel_dag_path装入函数集
    parent_obj = sel_dag_path_fn.parent(0)  # 调用函数集的parent方法获取父物体
    parent_obj_fn = OpenMaya.MFnDagNode(parent_obj)  # 将父对象装入函数集
    print(parent_obj_fn.name())  # 调用函数集name方法获得名称
    # 获取子物体
    child_obj_list = []
    for i in range(sel_dag_path_fn.childCount()):
        child_obj = sel_dag_path_fn.child(i)
        child_obj_fn = OpenMaya.MFnDagNode(child_obj)  # 将父对象装入函数集
        print(child_obj_fn.name())  # 调用函数集name方法获得名称
        child_obj_list.append(child_obj)

    sel_dag_path_fn.duplicate()  # 复制对象
    sel_dag_path_fn.setName('aaa')  # 重命名对象
    sel_dag_path_fn.removeChild(child_obj_list[-1])  # 移除子物体
    parent_obj_fn.addChild(child_obj_list[-1])  # 添加子物体


find_hierarchy()


#  创建节点
def create_node():
    parent_dag_path_fn = OpenMaya.MFnDagNode()  # 实例化MFnDagNode函数集
    parent_obj = parent_dag_path_fn.create("transform", "parent")  # 使用MFnDagNode类的方法创建节点

    child_dag_path_fn = OpenMaya.MFnDagNode()  # 实例化MFnDagNode函数集
    # 使用MFnDagNode类的方法创建节点，三个参数，节点类型，节点名称，节点父对象
    child_obj_a = child_dag_path_fn.create("transform", "childA", parent_obj)
    child_obj_b = child_dag_path_fn.create("transform", "childB", parent_obj)

    OpenMaya.MGlobal.deleteNode(child_obj_a)  # 删除节点


create_node()


# 遍历属性
def list_attr():
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected
    OpenMaya.MGlobal.getActiveSelectionList(selected)  # 获取当前选择对象装入选择列表
    obj = OpenMaya.MObject()  # 实例化MObject对象
    selected.getDependNode(0, obj)  # 将选择列表第一项获取依赖节点并装入MObject对象
    obj_dep_nod_fn = OpenMaya.MFnDependencyNode(obj)  # 获取依赖节点的函数集，用于操作依赖节点
    # 利用依赖节点函数集的attributeCount方法遍历属性
    for i in range(obj_dep_nod_fn.attributeCount()):  # attributeCount方法获取属性数量
        plug_obj = obj_dep_nod_fn.attribute(i)  # attribute方法获取属性
        plug = obj_dep_nod_fn.findPlug(plug_obj)  # findPlug方法获取属性接口
        print(plug.name())  # 打印属性名称


list_attr()


def get_set_attr():
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected
    OpenMaya.MGlobal.getActiveSelectionList(selected)  # 获取当前选择对象装入选择列表
    obj = OpenMaya.MObject()  # 实例化MObject对象
    selected.getDependNode(0, obj)  # 将选择列表第一项获取依赖节点并装入MObject对象
    obj_dep_nod_fn = OpenMaya.MFnDependencyNode(obj)  # 获取依赖节点的函数集，用于操作依赖节点

    tx_plug = obj_dep_nod_fn.findPlug("tx")  # 利用函数集方法findPlug，获取物体x轴移动的属性接口
    assert isinstance(tx_plug, OpenMaya.MPlug)  # 断言属性接口变量为OpenMaya.MPlug对象，方便自动补全
    print(tx_plug.asDouble())  # 用double类型打印属性tx_plug

    tx_plug.setDouble(3.7)  # 设置属性tx_plug值为3.7

    vis_plug = obj_dep_nod_fn.findPlug("visibility")  # 利用函数集方法findPlug，获取物体显示的属性接口
    assert isinstance(vis_plug, OpenMaya.MPlug)  # 断言vis_plug为为OpenMaya.MPlug对象，方便自动补全
    print(vis_plug.asBool())
    vis_plug.setBool(False)  # 设置vis_plug属性布尔值为关闭


get_set_attr()


def add_attr():
    """以下是OpenMaya.MFnAttribute的一些常见子类：
    OpenMaya.MFnNumericAttribute: 数字类属性，用于表示数值类型的属性，如浮点数、整数、布尔值等。
    OpenMaya.MFnTypedAttribute: 类型化属性，用于表示具有固定数据类型的属性，如字符串、向量、矩阵等。
    OpenMaya.MFnCompoundAttribute: 复合属性，用于表示由多个子属性组成的属性，如复合向量、复合颜色等。
    OpenMaya.MFnUnitAttribute: 单位属性，用于表示具有单位的数值属性，如长度、角度等。
    OpenMaya.MFnEnumAttribute: 枚举属性，用于表示具有预定义选项的属性，如下拉菜单的选项。
    OpenMaya.MFnMessageAttribute: 消息属性，用于表示连接到其他对象的消息传递属性。
    OpenMaya.MFnMatrixAttribute: 矩阵属性，用于表示矩阵类型的属性。
    OpenMaya.MFnGenericAttribute: 通用属性，用于表示没有特定数据类型的属性。
    OpenMaya.MFnLightDataAttribute: 光照数据属性，用于表示与光照相关的属性。

    MFnNumericAttribute一些常用的方法包括：
    create()：创建一个新的数字类属性对象。
    default()：设置属性的默认值。
    setMin()：设置属性的最小值。
    setMax()：设置属性的最大值。
    setKeyable()：设置属性是否可关键帧。
    setConnectable()：设置属性是否可连接。
    setWritable()：设置属性是否可写。
    """
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected
    OpenMaya.MGlobal.getActiveSelectionList(selected)  # 获取当前选择对象装入选择列表
    obj = OpenMaya.MObject()  # 实例化MObject对象
    selected.getDependNode(0, obj)  # 将选择列表第一项获取依赖节点并装入MObject对象
    obj_dep_nod_fn = OpenMaya.MFnDependencyNode(obj)  # 获取依赖节点的函数集，用于操作依赖节点
    #  OpenMaya.MFnNumericAttribute为 OpenMaya.MFnAttribute的子类之一，意为数字类属性
    fn_num_attr = OpenMaya.MFnNumericAttribute()  # 创建一个数字类属性实例
    # 属性的创建，第一个参数为属性长名称，第二个参数为属性短名称，第三个属性为数据类型为双精度浮点型，第四个属性为默认值
    attr_obj = fn_num_attr.create("myNewAttr", "MNA", OpenMaya.MFnNumericData.kDouble, 1.0)
    fn_num_attr.setKeyable(True)  # 属性设置为可尅帧
    obj_dep_nod_fn.addAttribute(attr_obj)  # 添加属性到attr_obj


add_attr()


def del_attr():
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected
    OpenMaya.MGlobal.getActiveSelectionList(selected)  # 获取当前选择对象装入选择列表
    obj = OpenMaya.MObject()  # 实例化MObject对象
    selected.getDependNode(0, obj)  # 将选择列表第一项获取依赖节点并装入MObject对象
    obj_dep_nod_fn = OpenMaya.MFnDependencyNode(obj)  # 获取依赖节点的函数集，用于操作依赖节点

    plug = obj_dep_nod_fn.findPlug("myNewAttr")  # 找到"myNewAttr"的属性接口
    assert isinstance(plug, OpenMaya.MPlug)  # 断言属性接口变量为OpenMaya.MPlug对象，方便自动补全
    attr_obj = plug.attribute()  # 通过属性接口找到对应属性
    obj_dep_nod_fn.removeAttribute(attr_obj)  # 移除该属性


del_attr()


def double_array_attr():
    """
    通过操纵双精度数组来操作蒙皮信息
    Returns:None

    """
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected
    selected.add("skinCluster1")  # 将名为"skinCluster1"的节点添加到选择列表selected中
    skin_cluster = OpenMaya.MObject()  # 实例化OpenMaya.MObject()创建一个MObject对象skin_cluster，用于存储皮肤集群节点。
    selected.getDependNode(0, skin_cluster)  # 将选择列表中的第一个节点作为依赖节点获取并存储到skin_cluster中

    skin_fn_node = OpenMaya.MFnDependencyNode(skin_cluster)  # 创建一个依赖节点函数集对象skin_fn_node，用于操作依赖节点
    skin_plug = skin_fn_node.findPlug("ptw")  # 找到名为"ptw"的属性接口skin_plug
    assert isinstance(skin_plug, OpenMaya.MPlug)  # 断言属性接口变量skin_plug是OpenMaya.MPlug对象，以便在编码时获得自动补全功能
    array_obj = skin_plug.asMObject()  # 将属性接口转换为MObject对象array_obj
    # 转化MObject对象为双精度数组数据函数集对象，用于操作双精度数组数据
    fn_doubel_array_data = OpenMaya.MFnDoubleArrayData(array_obj)
    weights = fn_doubel_array_data.array()  # 获取双精度数组属性的值，存储在weights变量中。
    assert isinstance(weights, OpenMaya.MDoubleArray)  # 断言weights变量是OpenMaya.MDoubleArray对象，以便获得自动补全功能
    # 遍历双精度数组属性的每个元素，并打印其值。然后使用weights.set(0.5, i)将每个元素的值设置为0.5。
    for i in range(weights.length()):
        print(weights[i])
        weights.set(0.5, i)

    new_array_obj = fn_doubel_array_data.create(weights)  # 创建新的双精度数组属性对象new_array_obj。
    skin_plug.setMObject(new_array_obj)  # 将新的双精度数组属性对象设置回原始的属性接口skin_plug。


double_array_attr()


def matrix_array():
    """
    处理矩阵数组
    Returns:None

    """
    """获取骨骼位置矩阵"""
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected。
    selected.add("joint2")  # 将名为"joint2"的节点添加到选择列表selected中。
    joint_obj = OpenMaya.MObject()  # 创建一个MObject对象joint_obj，用于存储选择列表中的第一个骨骼节点。
    selected.getDependNode(0, joint_obj)  # 将选择列表中的第一个节点获取并存储到joint_obj中。
    joint_fn_node = OpenMaya.MFnDependencyNode(joint_obj)  # 创建一个依赖节点函数集对象joint_fn_node，用于操作骨骼节点。
    matrix_plug = joint_fn_node.findPlug("matrix")  # 找到名为"matrix"的属性接口matrix_plug。
    assert isinstance(matrix_plug, OpenMaya.MPlug)  # 断言属性接口变量
    matrix_obj = matrix_plug.asMObject()  # 将属性接口转换为MObject对象matrix_obj。
    fn_matrix_data = OpenMaya.MFnMatrixData(matrix_obj)  # 创建一个矩阵数据函数集对象fn_matrix_data，用于操作矩阵数据。
    matrix = fn_matrix_data.matrix()  # 获取矩阵属性的值，存储在matrix变量中。
    """获取蒙皮节点bindPreMatrix绑定前矩阵，意为绑定姿态矩阵"""
    selected = OpenMaya.MSelectionList()  # 通过实例化OpenMaya.MSelectionList()创建一个选择列表对象selected。
    selected.add("skinCluster1")  # 将名为"skinCluster1"的节点添加到选择列表中。
    skin_obj = OpenMaya.MObject()  # 创建一个MObject对象skin_obj，用于存储选择列表中的第一个蒙皮节点。
    selected.getDependNode(0, skin_obj)  # 将选择列表中的第一个节点获取依赖节点并存储到skin_obj中。
    skin_fn_node = OpenMaya.MFnDependencyNode(skin_obj)  # 创建一个依赖节点函数集对象skin_fn_node，用于操作蒙皮节点。
    skin_plug = skin_fn_node.findPlug("bindPreMatrix")  # 找到名为"bindPreMatrix"的属性接口skin_plug。
    assert isinstance(skin_plug, OpenMaya.MPlug)  # 断言属性接口变量
    plug_0 = skin_plug.elementByLogicalIndex(1)  # 获取属性接口的第二个子接口，即数组的第二个元素，对应“joint2”的蒙皮。
    """设置绑定姿态矩阵为骨骼逆矩阵"""
    fn_matrix_data = OpenMaya.MFnMatrixData()  # 创建一个矩阵数据函数集对象fn_matrix_data。
    assert isinstance(matrix, OpenMaya.MMatrix)  # 断言matrix变量是OpenMaya.MMatrix对象。
    matrix_obj = fn_matrix_data.create(matrix.inverse())  # 创建一个新的矩阵对象matrix_obj，其中矩阵值为原始矩阵的逆矩阵。
    plug_0.setMObject(matrix_obj)  # 将新的矩阵对象设置到属性接口的第二个子接口中。


matrix_array()


def connect_attr():
    mul_fn_dag_node = OpenMaya.MFnDependencyNode()  # 创建一个依赖节点函数集对象mul_fn_dag_node。
    mul_fn_dag_node.create("multiplyDivide")  # 创建一个名为"multiplyDivide"的节点，并将函数集对象与该节点关联。
    output_plug = mul_fn_dag_node.findPlug("output")  # 找到名为"output"的属性接口output_plug。

    color_fn_dag_node = OpenMaya.MFnDependencyNode()  # 创建一个依赖节点函数集对象color_fn_dag_node。
    color_fn_dag_node.create("blendColors", 'blendColorsA')  # 创建blendColors节点名为blendColorsA
    input_plug = color_fn_dag_node.findPlug("color1")  # 找到名为"color1"的属性接口input_plug。

    modifier = OpenMaya.MDGModifier()  # 创建一个依赖图修改器对象modifier，用于连接属性。
    modifier.connect(output_plug, input_plug)  # 将output_plug和input_plug连接起来。
    modifier.doIt()  # 执行连接操作。

    color_fn_dag_node1 = OpenMaya.MFnDependencyNode()
    color_fn_dag_node1.create("blendColors", 'blendColorsB')
    input_plug1 = color_fn_dag_node1.findPlug("color1")

    modifier1 = OpenMaya.MDGModifier()
    modifier1.connect(output_plug, input_plug1)
    modifier1.doIt()

    outputs = OpenMaya.MPlugArray()  # 创建一个属性接口数组对象outputs，用于存储连接到output_plug的属性接口。
    assert isinstance(output_plug, OpenMaya.MPlug)  # 断言
    # 获取连接到output_plug的所有属性接口，包括输入和输出连接。三个参数，1：要链接的对象，2是否查询输入，3是否查询输出.
    output_plug.connectedTo(outputs, True, True)
    # 使用循环遍历outputs数组，并使用outputs[i].name()打印每个连接的属性接口的名称。
    for i in range(outputs.length()):
        print(outputs[i].name())


connect_attr()
