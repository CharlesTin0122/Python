import pymel.core as pm

selection = pm.selected()  # 根骨骼放入变量
joints = pm.ls(selection[0], dag=True, type="joint")  # 列出骨骼链的所有骨骼，注意参数dag
pm.select(joints)  # 选择所有骨骼


selection = pm.selected()  # 根骨骼放入变量
joints = pm.ls(selection[0], dag=True, type="constraint")  # 列出骨骼链的所有约束节点，注意参数dag
pm.select(joints)  # 选择所有约束节点
