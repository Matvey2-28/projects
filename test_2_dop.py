import random

def function(n, rd_numbers):
    numbers = [num for num in range(n) if num not in rd_numbers]
    if not numbers:
        return None
    return random.choice(numbers)

a = function(4, [1, 2, 3, 4, 5, 6, 7, 8, 9])
print(a)

