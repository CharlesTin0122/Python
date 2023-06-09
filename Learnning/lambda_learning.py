# -*- coding: utf-8 -*-
# @FileName :  lamda.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/8 11:18
# @Software : PyCharm
# Description:

"""--------------------------------------# 案例1----------------------------------"""

f = lambda x, y: x + y
print(f(1, 2))

"""#------------------------------------------- 案例2-----------------------------------"""

d = lambda x, y: x if x > y else y
print(d(1, 2))


"""---------------------------------------------# 案例3----------------------------------------"""

my_list = [
    ('a', 7),
    ('b', 9),
    ('c', 5),
    ('d', 1),
    ('e', 8),
    ('f', 3)
]

# sorted（）是一个排序迭代器（iterator），会迭代列表中的每一项进行升序排序，
# 参数1：为可迭代对象
# 参数key: 提供自定义键函数来自定义排序顺序，此处用匿名函数lambda将列表中每一项中的第二项为迭代key
# 参数reverse: 可以设置反向标志以降序请求结果。

sort_list = sorted(my_list, key=lambda x: x[1], reverse=True)
print(sort_list)

"""------------------------------------# 案例4 map 映射 lambda---------------------------------"""
# map()创建一个迭代器，使用来自每个可迭代对象的参数计算函数。
# 参数1：为一个函数
# 参数2：为一个可迭代对象
my_list1 = [1, 2, 3, 4, 5, 6, 7]
my_list2 = [7, 6, 5, 4, 3, 2, 1]

res1 = map(lambda x: x**2, my_list1)
print(list(res1))

res2 = map(lambda x, y: x + y, my_list1, my_list2)
print(list(res2))

"""-------------------------------reduce 归约--------------------------------"""
# 将两个参数的函数从左到右累积地应用于序列的项目，以便将序列减少为单个值。
# 例如，reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) 计算 ((((1+2)+3)+4)+5)。
# 参数1：为要使用的函数，参数2：为可迭代对象，参数3：为基础值
from functools import reduce
res = reduce(lambda x, y: x + y, range(1, 101))
print(res)


my_list3 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
res = reduce(lambda x, y: x + y, my_list3, 'xyz')
print(res)

"""-----------------------------------------filter过滤---------------------------------"""
# filter()返回一个迭代器，产生那些 function(item) 为真的可迭代对象。
# 如果 function 为 None，则返回为 true 的项
my_list4 = [1, 0, 0, 1, 0, 1, 0]
res = filter(lambda x: True if x == 1 else False, my_list4)
print(list(res))
