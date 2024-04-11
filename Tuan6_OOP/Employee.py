class Employee:
    def __init__(self, ID=None,name=None, department= None):
        self.ID = ID
        self.name = name
        self.department = department
    
    def working(self, task):
        self.task = task
        print(self.name+ ' is working '+task)
        
    def studying(self):
        print(self.name+ ' is studying '+self.task)
        
minh = Employee(ID=100,name='Minh',department='IT')
minh.working("in Lab")
minh.studying()