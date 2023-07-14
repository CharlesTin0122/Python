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
