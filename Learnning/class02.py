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


def make_noise(animal: Animal):
    animal.speak()


make_noise(dog)
make_noise(cat)

'''类的单例模式'''


# 创建类和变量来获取类
class StrTools:
    pass


str_tool = StrTools()
# 在另一个模块中导入另一个文件的类变量
from class02 import str_tool

# 创建变量来获取导入的类变量
s1 = str_tool()
s2 = str_tool()
# 这时两个类变量为同一个内存地址，
print(id(s1))
print(id(s2))


# 类的单例模式2
class Printer(object):
    tasks = []
    instance = None  # 存放第一个实例对象

    # 只有第一次实例化的时候正常进行，后面每次实例化，并不真的创建一个新实例
    def __new__(cls, *args, **kwargs):
        # 正常进行实例化，并把实例化后的对象 存在cls.instance里面
        if cls.instance is None:
            obj = object.__new__(cls)  # 实例化过程
            print(obj)
            cls.instance = obj  # 把实例化好的对象存下来
        # 以后每次实例化，直接返回第一次存的实例对象，在上一次实例对象基础上，再执行__init__
        return cls.instance

    def __init__(self, name) -> None:
        self.name = name

    def add_tasks(self, job):
        self.tasks.append(job)
        print('{} 添加任务 {}到打印机，总任务数{}'.format(self.name, job, len(self.tasks)))


p1 = Printer('word app')
p2 = Printer('ppt app')
p3 = Printer('excel app')
p1.add_tasks('word file')
p2.add_tasks('ppt file')
p3.add_tasks('excel file')
print(p1.name, p2.name, p3.name)

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
    def get_person(self, type):
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

'''类装饰器'''


# 类方法@classmethod，只能访问类变量，不能访问实例变量（__init__）
# 类方法使用了@classmethod之后，self接收的不再是实例化对象，而是类本身。

class Dog(object):
    name = 'stupid dog'  # 类变量

    def __init__(self, name) -> None:
        self.name = name  # 实例化对象传入name:DaHuang

    @classmethod  # 类方法装饰器
    def eat(self):
        print('-->', self)  # 会发现self此时是类本身<class '__main__.Dog'>，而不是实例化对象DaHuang
        print('dog {} is eating...'.format(self.name))  # 会发现self.name此时不是__init__中传入的DaHuang，而是类变量stupid dog

    @classmethod
    def run(cls):
        print(cls)


d = Dog('DaHuang')
d.eat()
d.run()


# 范例
class Students(object):
    __stu_Num = 0  # 类变量,私有变量

    def __init__(self, name) -> None:
        self.name = name  # 实例变量赋值
        self.__Add_stu()  # 初始化时直接调用类方法

    @classmethod
    def __Add_stu(cls):  # 私有类方法，外部无法调用
        cls.__stu_Num += 1  # 增加一个学生，学生数加一
        print('add a new sdudent:', cls.__stu_Num)


s1 = Students('xiaoming')
s2 = Students('xiaohong')
s3 = Students('xiaojun')


# 静态方法@staticmethod,不能访问类变量，也不能访问实例变量，隔离了它跟类和实例的任何关系
class Students(object):
    role = 'Stu'  # 类变量

    def __init__(self, name) -> None:
        self.name = name

    @staticmethod  # 静态方法
    def fly(self):  # 静态方法下self已失效
        print(self.name, 'is flying...')


s = Students('jack')
s.fly()
s.fly(s)


# 属性方法@property,把一个方法变成一个静态的属性（变量）
class Students(object):
    def __init__(self, name):
        self.name = name

    @property  # 属性方法
    def fly(self):
        print(self.name, 'is flying...')


s = Students('jack')
s.fly  # 调用属性无需使用括号


# 范例
class Flight(object):
    def __init__(self, name):
        self.flight_name = name

    def checking_status(self):
        print('connect airpot API...')
        print('checking flight {}status'.format(self.flight_name))
        return 1  # 1 arrived ,2 departured,3 cancle

    @property  # 属性方法
    def flight_status(self):  # get
        status = self.checking_status()
        if status == 0:
            print('flight got canceled...')
        elif status == 1:
            print('flight is arrived...')
        elif status == 2:
            print('flight has departured already...')
        else:
            print('can`t confirm')

    @flight_status.setter  # 属性方法设置属性
    def flight_status(self, status):
        print('changing...', status)
        self.status = status

    @flight_status.deleter  # 属性方法删除属性
    def flight_status(self):
        print('del...')


f = Flight('CA980')
f.flight_status
f.flight_status = 0
print(f.flight_status)
del f.flight_status
