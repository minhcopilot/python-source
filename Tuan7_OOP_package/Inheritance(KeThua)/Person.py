class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def info(self):
        print(self.name+",", self.age)
# create objects of Person class
john = Person("john", 36)
john.info()
Marry = Person("Marry",34)
Marry.info()

class Student(Person):
    def __init__(self, name, age,id):
        super().__init__(name, age)
        self.id = id
    def info(self):
        print(self.name, self.age, self.id)
        
class ExStudent(Student):
    def __init__(self,name,age,id,graduation_time):
        super().__init__(name,age,id)
        self.graduation_time=graduation_time
    def set_graduation_time(self,graduation_time):
        self.graduation_time=graduation_time
    def info(self):
        print(self.name, self.age, self.id, self.graduation_time)

ex_std = ExStudent("MinhExStuden",20,1,2024)
ex_std.info()
    


