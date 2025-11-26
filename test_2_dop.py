import random as rd

def function(n, rd_numbers):
    numbers = [num for num in range(n) if num not in rd_numbers]
    
    if not numbers:
        return None
    
    return rd.choice(numbers)

a = function(10, [1, 2, 3, 4, 5,])
print(a)

