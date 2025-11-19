counter = 0

def create_scope(default):
    counter = default * 2
    
    def nonlocal_print():
        nonlocal counter
        print(f'scoped {counter = }')
        
    def global_print():
        global counter
        print(f'global {counter = }')
        
    nonlocal_print()
    global_print()
    
create_scope(-4)