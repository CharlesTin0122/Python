# -*- coding: utf-8 -*-
# @FileName :  iterator_learn.py
# @Author   : TianChao
# @Email    : tianchao0533@gamil.com
# @Time     :  2023/6/8 15:55
# @Software : PyCharm
# Description:

# iterator迭代器：可迭代对象(iterable):list, tuple, string, set, dict, bytes
my_list = [1, 2, 3, 4, 5, 6, 7]
list_iter = iter(my_list)
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
