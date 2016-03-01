"""

Higher order functions
how to pass a list through a function
"""

def add_10(x):
    return 10 + x

li = [1,2,3]


for i in map(add_10, li):
    print(i)

"""
list comprehension


"""

[print(i) for i in map(add_10, li)]


"""

Class

"""

class Human(object):
    species = "H. sapiens"

    def __init__(self, name, ):
        self.name = name

    def say(self, msg):
        return "{name}: {message}".format(name=self.name, message=msg)

    @classmethod
    def get_species(cls):
        return cls.species
    @staticmethod
    def grunt():
        return "*grunt*"
aHuman = Human(name="bob")
# print(aHuman.say("Hi"))

print(id(aHuman))
# print(id(Human(name="Ian")))

bHuman = Human("Joel")
# print(bHuman.say("Hello"))

print(aHuman.get_species())

print(bHuman.get_species())

Human.species = "H. neanderthalensis"

print(bHuman.get_species())


print(Human.grunt())

class Animal(object):
    def __init__(self, name="unknown", words="nothing"):
        self.name = name
        self.words = words
        self.age = 0
        self.memories = []

    def __str__(self):
        return "i am a " + self.name + " and I say " + self.words

    def speak(self):
        print(self.words)

class Pig(Animal):
    def __init__(self, name="piggie", words="Oink"):
        #Animal.__init__(self, name, words)
        #super().__init__(name, words)
        super(Pig,self).__init__(name, words)



aAnimal = Animal()
print(aAnimal)

aPig = Pig()
print(aPig)






