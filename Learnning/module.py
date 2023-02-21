#模块和python标准库
import class02 as cl
HM1 = cl.Human("lao wang", 37, "male")
print(HM1.name)
cl.sayHello()

#范例2
from class02 import sayHello
sayHello()