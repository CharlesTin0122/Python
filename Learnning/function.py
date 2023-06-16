"""函数 function"""


def myfunc(name, age):  # 括号内为形参
    print("Hello! " + name)
    print(str(age) + " years old")


myfunc("Charles", 18)  # 括号内为实参


"""return返回值"""


def maxNum(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2


c = maxNum(6, 3)
print(c)


"""函数闭包"""


def outer(num1):  # 外部函数
    def inner(num2):  # 内部函数
        nonlocal num1  # 调用外部函数变量为可修改，类似于global
        num1 += num2  # 内外部函数参数相加等于外部函数参数
        print(num1)  # 输出外部函数参数

    return inner  # 返回内部函数


fn = outer(10)  # 外部函数实例化后成为内部函数
fn(10)  # 实例化内部函数
fn(10)  # 实例化内部函数


"""函数装饰器"""


def outer(func):
    def inner():
        print("I`m ly down")
        func()
        print("I`m get up")

    return inner


@outer  # 意为将下sleep函数作为参数填入outer函数，并执行返回inner函数
def sleep():
    import random
    import time

    time.sleep(random.randint(1, 5))
    print("I`m sleepping")


sleep()


"""以上案例和以下案例等同"""


def outer(func):
    def inner():
        print("I`m ly down")
        func()
        print("I`m get up")

    return inner


def sleep():
    import random
    import time

    time.sleep(random.randint(1, 5))
    print("I`m sleepping")


fn = outer(sleep)
fn()


""" 可变参数，关键字参数，参数的打包和解包"""


def print_info(name, age):
    print(f"my name is {name},and my age is {age}")


info_list = ["charles", 16]
print_info(*info_list)  # ‘*’可将参数列表解包成参数

info_dict = {"name": "tom", "age": 18}
print_info(**info_dict)  # "**"可将参数字典解包成参数


def print_args(*args):
    """
    可变参数
    """
    print(args)


print_args(1, 2, 3)  # 将多个参数打包成元组


def print_kwargs(**kwargs):
    print(kwargs)
    print("my name: ", kwargs.get("name"))
    print("my language: ", kwargs.get("language"))


print_kwargs(name="charles")
print_kwargs(name="tom", language="english")
