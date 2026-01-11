class Animal:
    pass

class pets(Animal):
    pass

class Dog(pets):
    @staticmethod
    def bark():
        print("Woof! Woof!")

d= Dog()
d.bark()