class Human():

    def __init__(self,name,age,sex): #构造函数 初始化函数
        self.name = name #成员变量
        self.age = age
        self.sex = sex

    def info(self): #类方法，成员函数
        print("My name is {}, {} years old and I'm a {}".format(self.name, self.age, self.sex))

Xiaoming = Human("xiao ming", 17, "male") #实例化
Xiaohong = Human("xiao hong", 19, "female")

print(Xiaoming.name)
Xiaohong.info()

def sayHello():
    print("Hello in class02!")