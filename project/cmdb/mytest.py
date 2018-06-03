#
# li=[
#     {'k':0,'age':19},
#     {'k':3,'age':18},
#     {'k':6,'age':21},
#     {'k':2,'age':24},
#     {'k':5,'age':20},
# ]
#
#
# new_li=sorted(li,key=lambda item:item['age'])
# print(new_li)

# class Dog(object):
#     color='black'
#     def __init__(self,name):
#         self.name = name
#
#     @classmethod
#     def eat(cls,):
#         print(cls.color)
#
#     def eat2(self):
#         print(self.color,self.name)
#
#     @staticmethod
#     def eat3():
#         print()
#
#
# d=Dog('jinmao')
# # Dog.eat()
# # d.eat2()
# d.color='yellow'
# # print(d.color)
# print(getattr(d,'color'))


# class ClassTest(object):
#     __num = 0
#
#     @classmethod
#     def addNum(cls):
#         cls.__num += 1
#
#     @classmethod
#     def getNum(cls):
#         return cls.__num
#
#     # 这里我用到魔术函数__new__，主要是为了在创建实例的时候调用人数累加的函数。
#     def __new__(self):
#         ClassTest.addNum()
#         return super(ClassTest, self).__new__(self)
#
#
# class Student(ClassTest):
#     def __init__(self):
#         self.name = ''
#
# a = Student()
# b = Student()
# print(ClassTest.getNum())


import time

class TimeTest(object):
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def showTime():
        return time.strftime("%H:%M:%S", time.localtime())


print(TimeTest.showTime())
t = TimeTest(2, 10, 10)
nowTime = t.showTime()
print(nowTime)

