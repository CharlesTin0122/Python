import os
import shutil


def move_files_to_root(root_dir):
    # 遍历指定目录下的所有根目录，目录和文件
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # 遍历所有文件
        for name in files:
            src_path = os.path.join(root, name) # 获取所有文件原路径
            dest_path = os.path.join(root_dir, name) # 获取所有文件目标路径
            # 判断文件是否已经存在，如果不存在，就将文件移动到根目录
            if not os.path.exists(dest_path):
                shutil.move(src_path, dest_path)
            # 如果文件已经存在，就跳过
            else:
                print(f"File {dest_path} already exists. Skipping {src_path}.")
        # 遍历所有子目录
        for name in dirs:
            dir_path = os.path.join(root, name) # 获取所有子目录原路径
            # 如果子目录为空，就删除它
            if not os.listdir(dir_path):
                os.rmdir(dir_path)


# 使用示例
root_directory = "D:\SSR_ZJB"
move_files_to_root(root_directory)
