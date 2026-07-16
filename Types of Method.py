class MathsOperation:
    factor = 2 #class argument
    def __init__(self,val):
        self.val = val

    # instance methods are methods which takes 'self' keyword as declaration
    def Multiplication(self):
        self.multiplied_val = self.val * self.factor
        print (f'The multiplied value of {self.val} and {self.factor} is {self.multiplied_val}')
        return self.multiplied_val
    @classmethod
    # class methods are methods that takes 'cls' keyword as its declaration. They are used to access class objects.
    def class_method(cls,value):
        cls.factor = value
        return cls.factor
    @staticmethod
    # static methods are methods which are independent of class and instance methods. They dont take any keyword for declaration.
    def addition(x,y):
        return x+y


obj = MathsOperation(10)
x = obj.Multiplication()
obj.class_method(3)
y = obj.Multiplication()

print(obj.addition(x,y))
