total = 0
class Student:
    id = name = age = sex = None
    __grade = None

    def __init__(self):
        self.id = 0
        self.__grade = "一年级"
        total = 10

    def printFun(self):
        print(self.__grade)

stu1 = Student()
stu1.printFun()
print(total)
