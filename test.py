class Printer(object):
	
	tasks = []
	instance = None #存放第一个实例对象
	
	def __new__(cls,*args,**kwargs):
		#正常进行实例化，并把实例化后的对象 存在cls.instance里面
		if cls.instance is None:
			obj = object.__new__(cls) #实例化过程
			print(obj)
			cls.instance = obj #把实例化好的对象存下来
		#以后每次实例化，直接返回第一次存的实例对象，在上一次实例对象基础上，再执行__init__
		return cls.instance 
	
	def __init__(self,name) -> None:
		self.name = name

	def add_tasks(self,job):
		self.tasks.append(job)
		print('{} 添加任务 {}到打印机，总任务数{}'.format(self.name,job,len(self.tasks)))
	#只有第一次实例化的时候正常进行，后面每次实例化，并不真的创建一个新实例

p1 = Printer('word app')
p2 = Printer('ppt app')
p3 = Printer('excel app')

p1.add_tasks('word file')
p2.add_tasks('ppt file')
p3.add_tasks('excel file')
print(p1.name,p2.name,p3.name)