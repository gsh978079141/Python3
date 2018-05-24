'''
Created on 2017年11月20日

@author: gdd
'''

class MyClass(object):
    '''
    classdocs
    '''
    __private__age=0
    __private__name=''


    def __init__(self,age,name):
        self.name=name
        self.age=age
        
    def myprint(self):
        print("姓名:%s\t年龄%d"%(self.name,self.age))
        
myclass=MyClass(10,"管生辉")
myclass.myprint()
print(MyClass.__dict__)
print(myclass.__getattribute__("name"))
print(MyClass.__name__)
print(MyClass.__doc__)
print(MyClass.__module__)
print(MyClass.__class__)
print(MyClass.__bases__)
class MyClass_Imp(MyClass):
    __private__sex=""
    def __new__(cls):
        print("MyClass_Imp_New        __new__方法调用")
   
    def MyClass_Imp_Print(self):
        print("MyClass_Imp_Print"+self.age)
        
myclass_imp=MyClass_Imp()
myclass_imp.MyClass_Imp_Print()