class Number1:
    def __init__ (self, val):
        self.val = val
        
    def __add__ (self, other):
        print('add', self.val, other)
        return self.val + other

    def __radd__ (self, other):
        print (' radd ', self.val, other)
        return other + self.val
      	
x = Number1(32)
y = Number1(25)
print(x + 1)
print(2 + y)
print(x + y)