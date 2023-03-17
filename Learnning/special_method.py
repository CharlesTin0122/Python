'''魔术方法'''
'''----------------------------基础魔术方法---------------------------'''
#__new__和__init__，可以让你改变从一个类建立一个对象时的行为
class A:
#__new__是从一个class建立一个object的过程
	def __new__(cls,x):
		print('__new__')
		return super().__new__(cls)
#__init__是有了这个object之后，给这个objct初始化的过程
	def __init__(self,x):
		self.x = x
		print('__init__')
#delete销毁实例化对象
	def __del__(self):
		print('__del__')
#representation，返回更详细的字符串
	def __repr__(self):
		return '<A>'
#string,返回人类更容易理解的字符串
	def __str__(self):
		return '<A>'
#format字符串格式化魔术方法
	def __format__(self, spec):
		if spec == 'x':
			return '0xA'
		return '<A>'
	
	def __bytes__(self):
		print('__bytes__called')
		return bytes([0,1])
'''
实例化的时候,先把class A作为参数传到__new__函数中,返回一个object
再把object作为变量去调用这个__init__函数
'''
#obj = __new__(A,1)
#__init__(obj,1)
o = A(1)
x = o
del o
print(A(1))
print(repr(A(1)))
print(str(A(1)))
print(f'{A(1)}',)
print(bytes(A(1)))
'''----------------------------------比较魔术方法----------------------------------'''
class Date:
	def __init__(self,year,month,date):
		self.year = year
		self.month = month
		self.date = date

	def __str__(self):
		return f'{self.year}/{self.month}/{self.date}'
#定义等于魔术方法，equal
	def __eq__(self, other):
		print('__eq__')
		print(self,other)
		return(self.year==other.year and
	 		self.month==other.month and
			self.date==other.date)
#定义不等于魔术方法not equal
#定义了等于魔术方法，可以不定义不等魔术方法，Python会自动取反
	def __ne__(self, other):
		print('__ne__')
		return(self.year!=other.year and
	 		self.month!=other.month and
			self.date!=other.date)
#定义大于魔术方法，greater than.
	def __gt__(self,other):
		if self.year > other.year:
			return True
		if self.year == other.year:
			if self.month > other.month:
				return True
			if self.month == other.month:
				return self.date > other.date
#定义小于魔术方法，less than
	def __lt__(self,other):
		if self.year < other.year:
			return True
		if self.year == other.year:
			if self.month < other.month:
				return True
			if self.month == other.month:
				return self.date < other.date
			
#定义大于等于魔术方法，greater than or equal to
	def __ge__(self,other):
		if self.year >= other.year:
			return True
		if self.year == other.year:
			if self.month >= other.month:
				return True
			if self.month == other.month:
				return self.date >= other.date
#定义小于等于魔术方法，less than or equal to
	def __le__(self,other):
		if self.year <= other.year:
			return True
		if self.year == other.year:
			if self.month <= other.month:
				return True
			if self.month == other.month:
				return self.date <= other.date
#定义哈希魔术方法
	def __hash__(self):
		return hash((self.year,self.month,self.date))
#定义布尔函数方法，在实例化后的条件语句（if）中使用	
	def __bool__(self):
		print('__bool__')
		return False
	
x = Date(2023,3,17)
y = Date(2023,3,18)
print(x,y)
print(x==y)
print(x!=y)
print(x>y)
print(x<y)
print(x>=y)
print(x<=y)
print(hash(x))
if x:
	print('True')
if not x:
	print('False')
