'''类的继承和多态'''
class Animal:
	def speak(self):
		pass
	
class Dog(Animal):
	def speak(self):
		print('wof wof wof !')

class Cat(Animal):
	def speak(self):
		print('meo meo meo !')



dog = Dog()
cat = Cat()

def make_noise(animal:Animal):
	animal.speak()

make_noise(dog)
make_noise(cat)


'''类的单例模式'''
#创建类和变量来获取类
class StrTools:
	pass
str_tool = StrTools()
#在另一个模块中导入另一个文件的类变量
from class02 import str_tool
#创建变量来获取导入的类变量
s1 = str_tool()
s2 = str_tool()
#这时两个类变量为同一个内存地址，
print(id(s1))
print(id(s2))




'''类的工厂模式'''
class Person:
	pass
class Worker(Person):
	pass
class Student(Person):
	pass
class Teacher(Person):
	pass

class Factory:
	def get_person(self,type):
		if type == 'w':
			return Worker()
		elif type == 's':
			return Student()
		else:
			return Teacher()
		
factory = Factory()
worker = factory.get_person('w')
stu = factory.get_person('s')
teacher = factory.get_person('t')
