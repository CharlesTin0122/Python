myListint = [1, 2, 3, 4, 5, 6]
myListStr = ["asd", "qwe", "zxc"]
myListint.append(8)  # append新增至最后
myListint.insert(2, 9)  # 在第几位插入某元素
del myListint[1]  # 删除第二项
a = myListint.pop(1)  # 取出第二项到a中
myListint.sort()  # 从小到大排序
myListLen = len(myListint)  # 列表位数
newList = myListint[0:3]  # 列表切片，只要前三项
newList = myListint[:-1]  # 列表切片，排除最后一项
newList = myListint[::2]  # 列表切片，步长为2
myListStr.remove("qwe")  # 列表中移除
print(myListint)
print(myListint[0])  # 0代表第一项
print(myListStr[-1])  # -1代表倒数第一项，-2代表倒是第二项。
print(myListLen)
print(newList)

"""-----append和extend的区别-----
# extend是将两个list合并成一个list，
# 而append是将传入的参数看做一个元素，拼接到上一个list后面。"""

# append()例子
list_all = []
list1 = [1, 2, 'cc', 'dd']
list2 = ['e', 3]
list_all.append(list1)
list_all.append(list2)
print(list_all)
# [[1, 2, 'cc', 'dd'], ['e', 3]]

# extend()例子
list_all = []
list1 = [1, 2, 'cc', 'dd']
list2 = ['e', 3]
list_all.extend(list1)
list_all.extend(list2)
print(list_all)
# [1, 2, 'cc', 'dd', 'e', 3]
