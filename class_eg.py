class MyClass:

	def __init__(self):
		self.myval = 0

	def get_value(self):
		print("In get method:")
		return  self.myval

	def set_value(self, value):
		print("In set method:")
		self.myval = value
		print("Setting value"+str(value))

obj = MyClass()
print(obj.get_value())
obj.set_value(4)
print(obj.get_value())
