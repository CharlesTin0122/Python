# -*- coding: utf-8 -*-
# @FileName :  generator_learn.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/8 17:03
# @Software : PyCharm
# Description:
"""------------------------------------案例1--------------------------"""

from collections.abc import Iterable
# ()推导式表示生成器，tuple()推导式表示元组推导式
gen = (x for x in range(1, 101))
print(isinstance(gen, Iterable))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))

for i in gen:
    print(i)

"""------------------------------------案例2----------------------------------"""


def fibonacci(n: int):
    """
    斐斐波那契数列
    Args:
        n: 数列迭代次数

    Returns:斐斐波那契数列列表

    """
    a, b = 0, 1
    res = []
    for count in range(0, n+1):
        res.append(a + b)
        a, b = b, a + b

    return res


print(fibonacci(10))


# 斐波那契数列生成器
def generator_fibonacci(n: int):
    """
    生成器方式实现斐波那契数列
    Args:
        n: 数列迭代次数

    Returns:斐斐波那契数列列表

    """
    a, b = 0, 1

    for count in range(0, n+1):
        yield a + b
        a, b = b, a + b


gen = generator_fibonacci(10)
next(gen)
for i in gen:
    print(i)
