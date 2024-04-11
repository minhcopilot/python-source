class Student:
    shool_name = "UTE"
    student_list = []
    def __init__(seft,id,name):
        seft.id = id
        seft.name = name
        seft.student_list.append(seft.name)

std1=Student(1,"Messi")
std2=Student(2,"Messi2")

print("shool_name",std1.shool_name)
print("student_list",std1.student_list)