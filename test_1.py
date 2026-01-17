def func_gen(break_key):
    num = 0
    while True:
        yield num ** 2
        
        if num == break_key:
            break
        
        num += 1
        
gen = func_gen(10)
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))
print(next(gen))