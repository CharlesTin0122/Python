'''-----------------------类 Class 面向对象-------------------------'''


class Player:
    def __init__(self, id, pos, speed, heal):
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


# 案例2

class Human:

    def __init__(self, name, age, sex):  # 构造函数 初始化函数
        self.name = name  # 成员变量
        self.age = age
        self.sex = sex

    def info(self):  # 类方法，成员函数
        print("My name is {}, {} years old and I'm a {}".format(self.name, self.age, self.sex))


Xiaoming = Human("xiao ming", 17, "male")  # 实例化
Xiaohong = Human("xiao hong", 19, "female")

print(Xiaoming.name)
Xiaohong.info()

'''----------------------------类的继承------------------------------------'''


class Human(object):

    def __init__(self, name, age):
        self.firstName = name.split()[0]
        self.lastName = name.split()[-1]
        self.age = age

    def greet(self):
        print("Hello, my name is %s. I am %s years old." % (self.firstName, self.age))

    def walk(self, steps=1):
        print("%s walked %s steps" % (self.firstName, steps))


class Canadian(Human):

    def __init__(self, name, age, city):
        # super()方法可以调用父类Human的函数，此案例中调用了父类父类Human的__init__函数。
        super(Canadian, self).__init__(name, age)
        self.city = city

    def greet(self):
        print("Hi, I'm %s from %s. I am %s years old eh!") % (self.firstName, self.city, self.age)


# Here are some examples of using a class
bob = Canadian('Bob Boberton', 45, 'Vancouver')
bob.greet()  # Hi I'm Bob from Vancouver. I am 45 years old eh!
bob.walk(5)  # Bob walked 5 steps

bob.age = 50
bob.greet()  # Hi I'm Bob from Vancouver. I am 50 years old eh!
'''类的模块导入'''


def sayHello():
    print("Hello in class02!")


'''私有属性和私有方法'''


class Phone:
    __current_voltage = None  # 私有变量（不可被外部调用）

    def __keep(self):  # 私有方法（不可被外部调用）
        print('a')


phone = Phone()
phone.__current_voltage()
phone.__keep()

'''神奇的反射'''


# 可以通过字符串的方式来操作对象的属性
class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        print('walking...')


p = Person('xiaoming', 20)

# 反射，映射，自省，共有四种方法，对应增删改查
# hasattr()
if hasattr(p, 'weight'):  # hasattr()通过字符串映射对象的方法存不存在
    print('has')

# getattr()
user_command = 'walk'
if hasattr(p, user_command):
    func = getattr(p, user_command)
    func()

# setattr()
# 增加属性
setattr(p, 'sex', 'Female')
print(p.sex)


# 增加方法
def talk(self):
    print(self.name, 'speaking...')


setattr(Person, 'speak', talk)
p.speak()

# delattr()
delattr(p, 'age')
p.age()

# 对模块进行反射
import sys

# for k, v in sys.modules.items():
# 	print(k,v)
print(sys.modules['__main__'])
mod = sys.modules[__name__]  # 获取当前模块
print(mod)
# 进行反射
if hasattr(mod, 'p'):
    o = getattr(mod, 'p')
    print(o)
print(p)
