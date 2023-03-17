'''正则表达式'''
#re.match()
import re
s = 'python charles python tin'
result = re.match('python',s) #从开头开始匹配，匹配成功返回匹配对象
print(result)
print(result.span())
print(result.group())

import re
s = '1python charles python tin'
result = re.match('python',s) #匹配不成功返回None
print(result)

#re.search()
import re
s = '1python666 python charles python tin'
result = re.search('python',s)#搜索整个字符串，从前向后，找到第一个就停止，不会像后
print(result)
print(result.span())
print(result.group())

import re
s = '1python666 python charles python tin'
result = re.search('python2',s) #匹配不成返回None
print(result)

#re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；
#re.search匹配整个字符串，直到找到一个匹配。


#re.findall()
import re
s = '1python666 python charles python tin'
result = re.findall('python',s)#匹配整个字符串，找出全部匹配项，
print(result)

#元字符匹配
'''
.  : 匹配任一字符（除了\n), \. : 匹配本身
[] : 匹配[]中列举的字符
\d :匹配数字,0-9
\D :匹配非数字
\s :匹配空白(空格,tab键)
\S :匹配非空白
\w :匹配单字字符,a-z,A-Z,0-9,_
\W :匹配非单子字符
'''
#数量匹配
'''
* :匹配前一规则的字符出现0至无数次
+ :匹配前一规则的字符出现1至无数次
? :匹配前一规则的字符出现0次或1次
{m} :匹配前一规则的字符出现m次
{m,} :匹配前一规则的字符出现最少m次
{m,n} :匹配前一规则的字符出现m到n次
'''
#边界匹配
'''
^ :匹配字符串开头
$ :匹配字符串结尾
\b:匹配一个单词的边界
\B:匹配非单词边界
'''
#分组匹配
'''
| :匹配左右任意一个表达式，表示“或”
():在括号中的字符表示一个分组
'''
import re
s = 'Charles_Tin0533 @@python3 !!64 ## it7'
result = re.findall(r'\d',s) # \d匹配数字，r表示字符串中转义字符无效，就是普通字符
print(result)

result = re.findall(r'\W',s) # \W匹配特殊字符
print(result)

result = re.findall(r'[a-zA-Z]',s) # 匹配[]中列举的字符,此范利表示找到所有的英文字母
print(result)

result = re.findall(r'[3-6]',s)
print(result)

'''复杂案例'''

#匹配账号，只能由字母和数字构成，长度6-10位
import re
# ^表示开头，$表示结尾，[]表示规则，{}表示位数
rule = '^[0-9a-zA-Z]{6,10}$' 
s = '1234567890123'
print(re.findall(rule,s))

#匹配qq号，5-11位数字，首位不为0
import re
# ^表示开头，$表示结尾，[]表示首位规则，\d表示剩余位规则，{}表示\d规则位数
rule = r'^[1-9]\d{4,10}&'
s = '02345678'
print(re.findall(rule,s))

#匹配邮箱地址，163，qq,gmail
import re
#a-bc.de_f.gh@163.com.cn
# ^表示开头，$表示结尾，[]表示规则，{}表示位数
rule = r'^[\w-]+(\.[\w-]+)*@(qq|163|gmail)(\.[\w-]+)+$' 
s = 'tianchao0533@163.com'
print(re.match(rule,s))