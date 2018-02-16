class MyClass:

	def __init__(self):
		self.myval = 0
		self.mylist = [1, 2, 3]

	def get_value(self):
		print("In get method:")
		return  self.myval

	def set_value(self, value):
		print("In set method:")
		self.myval = value
		print("Setting value : "+str(value))

	def handle_mutable(self, value):
		print("In handle_mutable method:")
		value.append(100)

	def handle_immutable(self, value):
		print("In handle_immutable method:")
		value = 100

obj = MyClass()
print(obj.get_value())
obj.set_value(4)
print(obj.get_value())
obj.handle_mutable(obj.mylist)
print("Value of list is {}".format(obj.mylist))
obj.handle_immutable(obj.mylist)
print("Value of list is {}".format(obj.myval))

