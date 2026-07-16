class A:
    def __init__(self):
        self._a = 10 #protected
        self.__b = 20 #private
        self.c = 30 #public

    def get_value(self):
        return self.__b

class B(A):
    def get_value(self):
        return self._a

class C(B):
    def get_value(self):
        return self._a

obj = A()
obj2 = B()
obj3 = C()
print(obj.get_value())
print(obj2.get_value())
print(obj3.get_value())

