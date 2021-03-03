
from singleton_decorator import singleton

@singleton
class Foo:
   def __init__(self):
       print('Foo created')

f = Foo() # Error, this isn't how you get the instance of a singleton
g = Foo()
#f = Foo.instance() # Good. Being explicit is in line with the Python Zen
#g = Foo.instance() # Returns already created instance
