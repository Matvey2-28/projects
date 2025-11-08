class Puppy:
    
    def __init__(self, index):
        self.index = index
        self.states = ['Болеет', 'Выздоравливает', 'Здоров']
        self.state = self.states[0]
        
    def get_treatment(self):
        if self.state == self.states[0]:
            state = states[1]
            
    def is_healthy(self):
        if self.state == self.states[2]:
            state = states[2]
            print(state)
        else:
            state = states[0]
            print(state)
            
class Dog:
    
    def __init__(self, klichka):
        self.klichka = klichka
        self.pup_list = {}
        
    def add_puppies(self, puppies):
        self.puppies = puppies
        for i in range(len(puppies)):
            self.pup_list[puppies[i]] = {}
            
    def add_state_off_puppy(self, puppy, states):
        self.puppy = puppy
        self.pup_list[puppy][states[0]]

    def heal_all(self):
        for puppie in self.pup_list:
            self.pup_list[puppies][states[1]] = []
    
    def all_are_healthy(self):
        for puppie in self.pup_list:
            if self.pup_list[puppies][states[2]]:
                print('Все щенки здоровы')
            else:
                print('Не все щенки здоровы')
                
    def give_away_all(self):
        for puppie in self.pup_list:
            if self.pup_list[puppies][states[2]]:
                pup_list.clear()
                
    def print_statistics(self):
        print(self.pup_list)
                
# class Vet:
    
#     def __init__(self, name, plant):
#         self.name = name
#         self.plant = plant
        
#     def work(self):
#         self.heal_all
#         print('Щенки лечатся')
        
#     def care(self):
#         if self.all_are_healthy:

        
        
        
        
        
        
        
        
        
        

        
        
# pup = Puppie('счастливый')
# pup.add_health('Генри', 9)
# pup.get_treatment() 
# pup.is_healthy() 
dog = Dog('Bulbochka')      
dog.add_puppies(['Генри', 'Antoshka'])
dog.add_state_off_puppy('Antoshka')
dog.print_statistics()

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            