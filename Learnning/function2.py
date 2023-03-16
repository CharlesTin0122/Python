'''递归:在满足条件的情况下，函数自己调用自己的一中特殊的的编程技巧'''
import os
def test_os():
	print(os.listdir(r'G:\Code\Python'))
	print(os.path.isdir(r'G:\Code\Python'))
	print(os.path.exists(r'G:\Code\Python'))
#获取文件夹下所有文件
def get_files_recursion(path):
	'''
	从指定的文件夹中使用递归方式获取全部的文件列表
	:param path:被判断的文件夹
	:return:包含全部的文件,如果目录无文件或者不存在则返回空
	'''
	print(f'当前判断的文件夹是:{path}')
	fileList = []
	if os.path.exists(path): #判断目录是存在
		for f in os.listdir(path): #遍历目录下所有文件
			newPath = path + '/' + f #文件名转换为路径
			if os.path.isdir(newPath): #判断文件为文件夹
				fileList += get_files_recursion(newPath) #调用函数递归，继续遍历文件夹，并添加到文件列表
			else: #判断文件不是文件夹
				fileList.append(newPath) #添加到路径变量

	else: #判断目录不存在
		print(f'指定的目录{path}不存在')#打印信息
		return []#返回空列表
	
	return fileList #返回文件列表


if __name__=='__main__':#判断为本文件运行
	print(get_files_recursion(r'G:\Code\Python'))#运行函数
