class Animal:
	def speak(self):
		pass
	
class Dog(Animal):
	def speak(self):
		print('wof wof wof !')

class Cat(Animal):
	def speak(self):
		print('meo meo meo !')



dog = Dog()
cat = Cat()

def make_noise(animal:Animal):
	animal.speak()

make_noise(dog)
make_noise(cat)