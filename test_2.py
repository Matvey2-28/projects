class Organic:
    def __init__(self, count_of_kletok):
        self.data = count_of_kletok
       
        
    def __add__(self, other):
        return Organic(self.data + other)
    
    def __sub__(self, other):
        return Organic(self.data - other)
    
    def __mul__(self, other):
        return Organic(self.data * other)
    
    def __truediv__(self, other):
        return Organic(self.data // other)
    
org = Organic(30)
result1 = org + 12
result2 = org - 12
result3 = org * 2
result4 = org / 12
print(result1.data)
print(result2.data)
print(result3.data)
print(result4.data)
        
