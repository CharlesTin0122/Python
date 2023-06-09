"""------------------------装饰器案例-----------------------------"""


def a_new_decorator(a_func):
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")

        a_func()

        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


def a_function_requiring_decoration1():
    print("I am the function which needs some decoration to remove my foul smell")


a_function_requiring_decoration1()
# outputs: "I am the function which needs some decoration to remove my foul smell"
a_function_requiring_decoration = a_new_decorator(a_function_requiring_decoration1)
# now a_function_requiring_decoration is wrapped by wrapTheFunction()
a_function_requiring_decoration()
# outputs:I am doing some boring work before executing a_func()
#        I am the function which needs some decoration to remove my foul smell
#        I am doing some boring work after executing a_func()

"""-----------------与以上代码块等价--------------------"""


@a_new_decorator
def a_function_requiring_decoration2():
    """Hey you! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")


a_function_requiring_decoration2()
# outputs: I am doing some boring work before executing a_func()
#         I am the function which needs some decoration to remove my foul smell
#         I am doing some boring work after executing a_func()

# the @a_new_decorator is just a short way of saying:
a_function_requiring_decoration2 = a_new_decorator(a_function_requiring_decoration1)

''' 
print(a_function_requiring_decoration.__name__)
# Output: wrapTheFunction
这并不是我们想要的！Ouput输出应该是"a_function_requiring_decoration"。
这里的函数被warpTheFunction替代了。它重写了我们函数的名字和注释文档(docstring)。
幸运的是Python提供给我们一个简单的函数来解决这个问题，那就是functools.wraps。我们修改上一个例子来使用functools.wraps：
'''


def a_new_decorator(a_func):
    @wraps(a_func)
    def wrapTheFunction():
        print("I am doing some boring work before executing a_func()")
        a_func()
        print("I am doing some boring work after executing a_func()")

    return wrapTheFunction


@a_new_decorator
def a_function_requiring_decoration():
    """Hey yo! Decorate me!"""
    print("I am the function which needs some decoration to "
          "remove my foul smell")


print(a_function_requiring_decoration.__name__)
# Output: a_function_requiring_decoration

"""-----------------------------蓝本规范-----------------------------------"""

from functools import wraps


def decorator_name(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print("run befor Function")
        func(*args, **kwargs)
        print("run after Function")

    return decorated


@decorator_name
def func_print():
    print("Function is running")


func_print()



