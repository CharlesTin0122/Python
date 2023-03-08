#类 Class 面向对象 面向过程
class Player():
    def __init__(self,id,pos,speed,heal):
        self.Id = id
        self.Position = pos
        self.Speed = speed
        self.Health = heal
pl1 = Player("xiaoming", [1.2, 1.3, 2.5], 1.0, 100.0)
pl2 = Player("xiaohong", [1.0, 0.3, 7.5], 1.5, 100.0)
print(pl1.Id)
print(pl1.Position)

print(pl2.Id)
print(pl2.Position)

#案例2

class Human():

    def __init__(self,name,age,sex): #构造函数 初始化函数
        self.name = name #成员变量
        self.age = age
        self.sex = sex

    def info(self): #类方法，成员函数
        print("My name is {}, {} years old and I'm a {}".format(self.name, self.age, self.sex))

Xiaoming = Human("xiao ming", 17, "male") #实例化
Xiaohong = Human("xiao hong", 19, "female")

print(Xiaoming.name)
Xiaohong.info()


class Human():

	def __init__(self,name,age,sex): #构造函数 初始化函数
		self.name = name #成员变量
		self.age = age
		self.sex = sex

	def info(self): #类方法，成员函数
		print("My name is {}, {} years old and I'm a {}".format(self.name, self.age, self.sex))

Xiaoming = Human("xiao ming", 17, "male") #实例化
Xiaohong = Human("xiao hong", 19, "female")

print(Xiaoming.name)
Xiaohong.info()

def sayHello():
	print("Hello in class02!")


class Phone:
	__current_voltage = None #私有变量（不可被外部调用）
	def __keep(self): #私有方法（不可被外部调用）
		print('a')
phone = Phone()
phone.__current_voltage()
phone.__keep()
