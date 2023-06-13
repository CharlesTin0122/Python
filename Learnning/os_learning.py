import json
import os
# 系统相关内容
print(os.name)  # 系统名称
print(os.environ)  # 环境变量
print(os.sep)  # 获取当前平台分隔符 "\"
print(os.pathsep)  # 获取当前平台路径分隔符 ";"
print(os.getcwd())  # 获取文件所在目录
# 文件和目录操作
os.mkdir("test")  # 创建目录
os.rmdir("test")


def main():
    print(os.getcwd())  # 获取当前maya执行路径

    filePath1 = os.path.abspath('__file__')  # 当前脚本绝对路径（包含文件名）
    filePath2 = os.path.dirname(filePath1)  # 当前脚本所在的位置（不包含文件名）

    os.chdir(filePath2)  # 切换maya执行路径

    print(os.getcwd())
    with open("path.json", "r") as f:
        data = json.load(f)
    print(data)




# 删除文件
os.remove(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
# 重命名文件
os.rename(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt',
          r'D:\Backup\Documents\maya\2020\prefs\scripts\nodelete.txt')
# 分割文件的路径和文件名
os.path.split(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
# 获取路径
os.path.dirname(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
# 获取文件名
os.path.basename(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
# 提取文件扩展名
os.path.splitext(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
#  : 将path进行组合，若其中有绝对路径，则之前的path将被删除。
os.path.join(path1, path2)

filePath = os.path.abspath('__file__')
print(filePath)


# 通过os.path.walk递归遍历，可以访问子文件夹
def file_name_walk(file_dir):
    for parent, dirnames, filenames in os.walk(file_dir):
        # 显示所有子目录路径
        for dirname in dirnames:
            print(os.path.join(parent, dirname))
        # 显示目录下所有文件
        for filename in filenames:
            print(os.path.join(parent, filename))
