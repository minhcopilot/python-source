class Shape():
    def __init__(self):
        pass
    def get_area(self):
        pass
    
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def get_area(self):
        return self.width * self.height
    
class Circle(Shape):
    def __init__(self,radius):
        self.radius = radius
    def get_area(self):
        return self.radius * self.radius * 3.14

r1 =Rectangle(1,5)
c1 =Circle(3)
shapes = [Rectangle(2, 5), Circle(3)]
print(r1.get_area(),c1.get_area())
print("Area of rectangle is:", str(shapes[0].get_area()))
print("Area of circle is:", str(shapes[1].get_area()))