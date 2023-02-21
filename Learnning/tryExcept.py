try:
    print(a)
    print("123")
    a = 1/0
except NameError:
    print("变量没有声明")
except ZeroDivisionError:
    print("除等于零")
except Exception as e:
    print (e)

finally:
    print("hello world!!!")