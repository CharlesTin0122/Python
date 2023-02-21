import json
import os

def main():
    print(os.getcwd()) #获取当前maya执行路径

    filePath = os.path.abspath('__file__') #当前脚本绝对路径（包含文件名）
    filePath2 = os.path.dirname(filePath) #当前脚本所在的位置（不包含文件名）

    os.chdir(filePath2) #切换maya执行路径

    print(os.getcwd())
    with open("path.json", "r") as f:
        data = json.load(f)
    print(data)

#获取当前平台分隔符
os.sep
#删除文件
os.remove(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
#重命名文件
os.rename(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt',r'D:\Backup\Documents\maya\2020\prefs\scripts\nodelete.txt')
#分割文件的路径和文件名
os.path.split(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
#获取路径
os.path.dirname(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
#获取文件名
os.path.basename(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt')
#提取文件扩展名
os.path.splitext(r'D:\Backup\Documents\maya\2020\prefs\scripts\delete.txt') 

filePath = os.path.abspath('__file__')
print(filePath)