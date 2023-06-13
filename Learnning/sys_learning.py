import sys
print(sys.path)  # 检索python解释器的环境路径
print(sys.version)  # 检索python解释器的版本
print(sys.argv)  # 检索python文件的参数列表
print(sys.platform)  # 检索python解释器的平台
print(sys.maxsize)  # 检索python解释器的平台
print(sys.getdefaultencoding())  # 检索python默认编码
print(sys.getfilesystemencoding())  # 检索python文件系统默认编码
print(sys.getrecursionlimit())  # 获取python递归次数限制
print(sys.setrecursionlimit(1000))  # 设置python递归次数限制

sys.path.append(r'G:\Code\Python')
sys.exit(0)  # 退出状态码
