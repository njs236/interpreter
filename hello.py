import sys
import io
import os

print("Hello")
print("World")

class Shape:
    __name = ""
    def __init__(self, name):
        self.__name = name

    def Area(self):
        return


class Rectangle:
    __width = ""
    __height = ""
    def __init__(self, width, height):
        self.__width = width
        self.__height = height

    def Area(self):
        return self.__width * self.__height

bob = Rectangle(3, 4)
print(bob.Area())

try:
    raise IndexError("This is an index error")
except IndexError as e:
    pass
except {TypeError, NameError}:
    pass
else:
    print("All Good!")
"""
def add(x, y):
        return x + y

sum=add(2,3)
print(sum)
"""
"""

    tuple returned when passing parameters in the next function
"""
"""
def add(*args):
    print args

add(1,2,3,4,5,6,7)

"""
"""
def add(x,y):
    return 2*x + y
sum = add(y=2, x=3)
print(sum)
"""

def keyword_args(**kwargs):
    return kwargs

keyword_args(big="foot", lock="ness")


"""

Next example is scope error
"""
def setX(num):
    global x
    x = num
    print(x)

setX(2)
print(x)

"""
nested function

"""

def create_adder(x):
    def adder(y):
        return x*2+ y
    return adder

add_10 = create_adder(10)
print(add_10(3))

x=5
x = x**x
print("x = " + str(x))

g = 5
h = 7
h = g+h
print("h = " + str(h))

w = 7 % 3
print("w = " + str(w))

z = 5
z += 2
print ("z = " + str(z))

a = 45
a *= 3
print ("a = " + str(a))

"""

list, tuples, and strings and dictionaries exercises

"""


"""
first example cannot be done with python 3

a = str(int(2.23) + float(14)) + "tomatoes"

a should be 16.000 tomatoes

"""

print("ham Ham".upper())

print("SUPER baby".lower())

b = "I am ham"
print(b.split())

print(b.split("m"))

"""
this next one will nt work as a is not defined

b.join(a)
"""
c = "int: %d, float %.5f" % (14.4, 55.2)


L = [1,6,7,26,8,3,4,5]
print(L[:])
print(L[:2])
print(L[2:])
print(L[::2])
print(L[1::2])




