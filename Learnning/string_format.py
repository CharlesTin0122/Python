string1 = "hello \nworld" #\n=换行
print(string1)

string2 = "hello \tworld" #\t=缩进（4个空格）
print(string2)

string3 = "hello \\world" #\\=\
print(string3)

#'a',"a",\"a\",\'a\'
string4 = "polySelectEdgesEveryN \"edgeRing\" 2;"
print(string4)

#格式化字符串
i = 'world'
a = '!!!'
string5 ='hello {} {}'.format(i,a)
print(string5)