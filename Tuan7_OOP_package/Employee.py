class Employee:
    def __init__(self, ID,name, salary):
        self.ID = ID
        self.name = name
        self.__salary = salary # salary là một private property
    def set_salary(self, salary):
        self.__salary = salary
    def display_salary(self): # display_salary là một public method
        print("Salary:", self.__salary)

steve = Employee(1,'Minh', 2500)
steve.display_salary()
steve.set_salary(124)
steve.display_salary()