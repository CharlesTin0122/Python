# -*- coding: utf-8 -*-
# @FileName :  test.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/1 11:29
# @Software : PyCharm
# Description:
import os
from fbx_scene import FbxClass


def remove_fbx_obj(input_path: str, remove_obj: list, output_path: str) -> None:
    """
    批量移除一批fbx文件中的某些对象
    Args:
        input_path: 输入fbx文件路径
        remove_obj: 要移除的对象列表
        output_path: 输出fbx文件路径

    Returns:None

    """
    fbx_paths = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            fbx_paths.append(file_path)
    print(fbx_paths)
    print(len(fbx_paths))

    for fbx_path in fbx_paths:
        fbx_file = FbxClass(fbx_path)
        try:
            fbx_file.remove_nodes_by_names(remove_obj)
        except Exception as exc:
            print(exc)
        try:
            fbx_file.save(
                filename=os.path.join(output_path, os.path.basename(fbx_path))
            )
        except Exception as e:
            print(e)


if __name__ == '__main__':
    input_path1 = r"D:\Work_MobilGame\outsourcing\Submissions\move"
    remove_obj1 = ["weapon_R"]
    output_path1 = r"D:\Work_MobilGame\outsourcing\Submissions\modify"

    remove_fbx_obj(input_path1, remove_obj1, output_path1)
