counter = 0 

def update(value):
    global counter
    result = counter + value
    
    print(f'{counter} + {value} = {result}')
    counter = result
    
update(1)
update(2)
update(5)

print(f'{counter = }')