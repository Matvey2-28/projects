class MyClass:
    counts = 0
    
    def __init__(self):
        MyClass.counts = MyClass.counts + 1
        
    @classmethod 
    def classmethod(cls):
        print(cls.counts)
        
        
MyClass.classmethod()
mc1 = MyClass()
mc2 = MyClass()
mc3 = MyClass()

MyClass.classmethod()