import time

class Player:
    
    level = 0
    
    def __init__(self, username):
        self.username = username
        self.varrior_list = {}
        
    def create_varriors(self, varriors):
        self.varriors = varriors
        for i in range(len(varriors)):
            self.varrior_list[varriors[i]] = {}
            
    def select_varrior(self, varrior):
        self.varrior = varrior
        self.varrior_list[varrior][level]
            
    def complete_task(self):
        print('Задание выполняется')
        time.sleep(60)
        print('Воин выполнил поручение от героя')
        self.varrior(level)
        
        
            
    
            

# class Varrior:
    
#     def __init__(self, name):
#         self.name = name
        
#     def go_ahead(self):
        
pl = Player('Matvik228')
pl.create_varriors(['Jamal', 'Makan'])
pl.select_varrior('Jamal')
pl.complete_task()