#函数 function
def myfunc(name,age): #括号内为形参
    print("Hello! " + name)
    print(str(age) + " years old")

myfunc("Charles",18) #括号内为实参

#范例2 return返回值
def maxNum(num1,num2):
    if num1 > num2:
        return num1
    else:
        return num2

c = maxNum(6,3)
print(c)