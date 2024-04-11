class Person():
    
    def __init__(self,age):
        self.__age = 20
    def show_age(self):
        print(self.__age)
    def set_age(self,age):
        self.__age = age

p1 = Person(30)
p1.show_age()
p1.set_age(18)
p1.show_age()

