#模块和python标准库
import class02 as cl
HM1 = cl.Human("lao wang", 37, "male")
print(HM1.name)
cl.sayHello()

#范例2
from class02 import sayHello
sayHello()

#当模块被导入的情况下，模块中的__name__返回的是模块名：xxx.py。
print(__name__)#当模块本身在运行时，返回的是__main__,代表模块本身。

if __name__ == '__main__':
	print('程序自身在运行')
else:
	print('我来自另一模块')

#字符串方式导入模块
import importlib
importlib.import_module('class02')
importlib.import_module('fbxExporter.fbxExporter01')