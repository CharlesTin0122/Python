#案例1
correctPw = "123456"
inputPW = input("Input your password: ")

while inputPW != correctPw:
    print("Incorrect!!!")
    inputPW = input("Input your password: ")

print("Password correct")

#案例2
correctPw = "123456"
while True:
    inputPW = input("Input your password: ")
    if inputPW == correctPw:
        print("Password correct")
        break
    else:
        print("Incorrect!!!")