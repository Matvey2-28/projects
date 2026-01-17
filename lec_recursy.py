def fibonachi_num(n):
    if n <= 1:
        return n
    else:
        return (fibonachi_num(n-1) + fibonachi_num(n-2))
    
n = 5

for i in range(n):
    print(fibonachi_num(i))