'''魔术方法'''
'''----------------------------基础魔术方法---------------------------'''


# __new__和__init__，可以让你改变从一个类建立一个对象时的行为
class A:
    # __new__是从一个class建立一个object的过程
    def __new__(cls, x):
        print('__new__')
        return super().__new__(cls)

    # __init__是有了这个object之后，给这个objct初始化的过程
    def __init__(self, x):
        self.x = x
        print('__init__')

    # delete销毁实例化对象，对应实例化后del()命令
    def __del__(self):
        print('__del__')

    # 改变对象的字符串显示格式
    # representation，返回更详细的字符串
    def __repr__(self):
        return '<A>'

    # string,返回人类更容易理解的字符串
    def __str__(self):
        return '<A>'

    # format字符串格式化魔术方法
    def __format__(self, spec):
        if spec == 'x':
            return '0xA'
        return '<A>'

    def __bytes__(self):
        print('__bytes__called')
        return bytes([0, 1])


'''
实例化的时候,先把class A作为参数传到__new__函数中,返回一个object
再把object作为变量去调用这个__init__函数
'''
# obj = __new__(A,1)
# __init__(obj,1)
o = A(1)
x = o
del o
print(A(1))
print(repr(A(1)))
print(str(A(1)))
print(f'{A(1)}', )
print(bytes(A(1)))
'''----------------------------------比较魔术方法----------------------------------'''


class Date:
    def __init__(self, year, month, date):
        self.year = year
        self.month = month
        self.date = date

    def __str__(self):
        return f'{self.year}/{self.month}/{self.date}'

    # 定义等于魔术方法，equal
    def __eq__(self, other):
        print('__eq__')
        print(self, other)
        return (self.year == other.year and
                self.month == other.month and
                self.date == other.date)

    # 定义不等于魔术方法not equal
    # 定义了等于魔术方法，可以不定义不等魔术方法，Python会自动取反
    def __ne__(self, other):
        print('__ne__')
        return (self.year != other.year and
                self.month != other.month and
                self.date != other.date)

    # 定义大于魔术方法，greater than.
    def __gt__(self, other):
        if self.year > other.year:
            return True
        if self.year == other.year:
            if self.month > other.month:
                return True
            if self.month == other.month:
                return self.date > other.date

    # 定义小于魔术方法，less than
    def __lt__(self, other):
        if self.year < other.year:
            return True
        if self.year == other.year:
            if self.month < other.month:
                return True
            if self.month == other.month:
                return self.date < other.date

    # 定义大于等于魔术方法，greater than or equal to
    def __ge__(self, other):
        if self.year >= other.year:
            return True
        if self.year == other.year:
            if self.month >= other.month:
                return True
            if self.month == other.month:
                return self.date >= other.date

    # 定义小于等于魔术方法，less than or equal to
    def __le__(self, other):
        if self.year <= other.year:
            return True
        if self.year == other.year:
            if self.month <= other.month:
                return True
            if self.month == other.month:
                return self.date <= other.date

    # 定义哈希魔术方法
    def __hash__(self):
        return hash((self.year, self.month, self.date))

    # 定义布尔函数方法，在实例化后的条件语句（if）中使用
    def __bool__(self):
        print('__bool__')
        return False


x = Date(2023, 3, 17)
y = Date(2023, 3, 18)
print(x, y)
print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)
print(hash(x))
if x:
    print('True')
if not x:
    print('False')

'''-------------------对象属性相关的魔术方法-------------------'''


class A:
    def __init__(self):
        self.exist = 'abc'
        self.counter = 0

    # 当实例化对象调用的属性不存在的时候，希望她做点什么
    def __getAttr__(self, name):
        print('getting{}'.format(name))
        # raise手动设置异常
        raise AttributeError

    # 只要你尝试去读取它的属性，就会被调用
    def __getattribute__(self, name):
        if name == 'data':
            self.counter += 1
        return super().__getattribute__(name)


o = A()
# o.test属性并不存在
print(o.test)
print(o.data)
print(o.counter)

'''------------------item系列魔术方法----------------------'''


# 把一个对象变成字典，像字典一样增删改查
class Human:
    def __init__(self, name):
        self.name = name

    # 把一个对象变成字典
    def __getitem__(self, item):
        # 打印对象属性的键值对
        print(self.__dict__)
        print('获取key', item)
        # 打印属性的值
        print(self.__dict__[item])

    # 可以让对象设置属性
    def __setitem__(self, key, value):
        print('设置key', key)
        self.__dict__[key] = value

    # 可以让对象删除属性
    def __delitem__(self, key):
        print('del obj[key]时，我执行')
        self.__dict__.pop(key)

    def __delattr__(self, item):
        print('del obj.key时,我执行')
        self.__dict__.pop(item)


# 实例化对象
b = Human('abc')
# 查看属性的值
b['name']
# 修改属性的值
b['name'] = 'cde'
print(b.name)

# 设置属性的值
b['age'] = 64
# 打印属性的值
print(b.age)
# 删除属性
del b['name']
del b.age
'''-------------------------------重要的魔术方法-------------------------'''


# str，repr改变对象的字符串显示格式，del 析构方法
class School:
    def __init__(self, name, addr, type):
        self.name = name
        self.addr = addr
        self.type = type

    def __repr__(self) -> str:
        return 'School({},{})'.format(self.name, self.addr)

    def __str__(self) -> str:
        return '({},{})'.format(self.name, self.addr)

    def __del__(self):
        print('对象被释放了...')


s1 = School('yinshanhu', 'suzhou', 'xiaoxue')
print(repr(s1))
print(str(s1))
print(s1)
del s1
'''
str函数或print函数调用时--->__str__()
repr函数或交互式解释器调用时--->—__repr__()
如果__str__没有被定义,那么就会使用__repr__代替输出
这两个方法的返回值必须是字符串，否则会抛出异常
'''


# __new__方法，在__init__之前执行
class Student(object):
    def __init__(self, name) -> None:
        self.name = name
        print('init')

    # __new__是从一个class建立一个object的过程,负责执行__init__,进行实例初始化之前的工作
    def __new__(cls, *args, **kwargs):
        print(cls, args, kwargs)
        # 必须返回，执行父类的__new__放法,否则__init__不执行
        return object.__new__(cls)
    # return super().__new__(cls)


p = Student('xiaoming')
p.name


# 范例,单例模式
class Printer(object):
    tasks = []
    instance = None  # 存放第一个实例对象

    def __init__(self, name) -> None:
        self.name = name

    def add_tasks(self, job):
        self.tasks.append(job)
        print('{} 添加任务 {}到打印机，总任务数{}'.format(self.name, job, len(self.tasks)))

    # 只有第一次实例化的时候正常进行，后面每次实例化，并不真的创建一个新实例
    def __new__(cls, *args, **kwargs):
        # 正常进行实例化，并把实例化后的对象 存在cls.instance里面
        if cls.instance is None:
            obj = object.__new__(cls)  # 实例化过程
            print(obj)
            cls.instance = obj  # 把实例化好的对象存下来
        # 以后每次实例化，直接返回第一次存的实例对象，在上一次实例对象基础上，再执行__init__
        return cls.instance


p1 = Printer('word app')
p2 = Printer('ppt app')
p3 = Printer('excel app')

p1.add_tasks('word file')
p2.add_tasks('ppt file')
p3.add_tasks('excel file')
print(p1.name, p2.name, p3.name)
