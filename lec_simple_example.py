class Number:
    def __init__(self, value):
        self.data = value
        
    def __add__(self, other):
        return Number(self.data + other)
    
    
a = Number(12)
b = a + 4
print(b.data)