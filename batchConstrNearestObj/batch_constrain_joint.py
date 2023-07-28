# coding: utf-8
# @Time    : 2023/4/3 13:32
# @Author  : TianChao
# @File    : test001.py
# @Email: tianchao0533@gamil.com
# @Software: PyCharm

import pymel.core as pm


class BatchConstrNearestObj(object):
    def __init__(self):
        self.window = None
        self.list1_ui = None
        self.list2_ui = None
        self.list1 = []
        self.list2 = []
        self.constrain_list = []

    def create_ui(self):
        """创建UI"""
        self._delete_existing_window()
        self.window = pm.window("MyWin", title="Batch Constrain Tool")
        with pm.columnLayout(rowSpacing=5, adj=True):
            with pm.frameLayout(label="BatchConstrNearestObj"):
                with pm.columnLayout(adj=1):
                    pm.button(
                        label="Load Constrain Obj", w=150, h=30, c=self.load_list1_click
                    )
                with pm.scrollLayout(
                    w=200, h=150, bgc=(0.5, 0.5, 0.5)
                ) as self.list1_ui:
                    pm.text("Obj List A:")
                with pm.columnLayout(adj=1):
                    pm.button(
                        label="Load be Constrained Obj",
                        w=150,
                        h=30,
                        c=self.load_list2_click,
                    )
                with pm.scrollLayout(
                    w=200, h=150, bgc=(0.5, 0.5, 0.5)
                ) as self.list2_ui:
                    pm.text("Obj List B:")
                with pm.columnLayout(adj=1):
                    pm.button(
                        label="Batch Constrain !!!", w=150, h=50, c=self.batch_constrain
                    )
        self.window.show()

    def _delete_existing_window(self):
        """清除已存在的窗口"""
        try:
            pm.deleteUI("MyWin")
        except RuntimeError as exc:
            print(exc)

    def _display_objects_in_ui(self, obj_list, ui_layout):
        """在窗口中列出所选对象

        Args:
            obj_list (list): 所选对象列表
            ui_layout (_type_): 要列出对象的窗口
        """
        with ui_layout:
            for obj in obj_list:
                pm.text(label=str(obj))

    def load_list1_click(self, *args):
        """按钮点击函数

        Returns:
            list: 对象列表
        """
        self.list1 = pm.selected()
        if not self.list1:
            pm.warning("No selected obj !!!")
            return
        self._display_objects_in_ui(self.list1, self.list1_ui)
        return self.list1

    def load_list2_click(self, *args):
        """按钮点击函数

        Returns:
            list: 对象列表
        """
        self.list2 = pm.selected()
        if not self.list2:
            pm.warning("No selected obj !!!")
            return
        self._display_objects_in_ui(self.list2, self.list2_ui)
        return self.list2

    def _find_closest_object(self, obj):
        """找到最近的对象

        Args:
            obj (_type_): 对象A

        Returns:
            _type_: 距离对象A最近的对象B
        """
        closest_obj = None
        closest_distance = float("inf")
        pos1 = obj.getTranslation(space="world")
        for other_obj in self.list2:
            if other_obj == obj:
                continue
            pos2 = other_obj.getTranslation(space="world")
            distance = (pos1 - pos2).length()
            if distance < closest_distance:
                closest_obj = other_obj
                closest_distance = distance
        return closest_obj

    def batch_constrain(self, *args):
        """批量父子约束

        Returns:
            _type_: 约束列表
        """
        self.constrain_list = []
        for obj in self.list1:
            closest_obj = self._find_closest_object(obj)
            if closest_obj and not pm.listConnections(
                closest_obj, type="parentConstraint"
            ):
                pm.parentConstraint(obj, closest_obj, maintainOffset=True)
                constrain_list = f"{obj}->{closest_obj}"
                self.constrain_list.append(constrain_list)
        print(self.constrain_list)
        return self.constrain_list


if __name__ == "__main__":
    ui = BatchConstrNearestObj()
    ui.create_ui()
