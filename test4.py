import numpy as np

def function(a, b, N):
    x = np.linspace(a, b, N)
    y = x ** 2
    print(y)
    
function(1, 10, 1000)