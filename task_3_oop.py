class Puppy:
    
    states = ['Болеет', 'Выздоравливает', 'Здоров']
    
    def __init__(self, index):
        self.index = index
        self.states = ['Болеет', 'Выздоравливает', 'Здоров']
        self.state = self.states[0]
        
    def get_treatment(self):
        c_index = self.states.index(self.state)
        if c_index < (self.states) - 1:
            self.state = self.states[c_index + 1]
            return True
        return False
            
    def is_healthy(self):
        return self.state == self.states[2]
    
    def info(self):
        return {'index': self.index, 'state': self.state, 'is_healthy': self.is_healthy()}
            
    def 
class Dog:
    
    def __init__(self, pup_count):
        self.puppies = [Puppy(i) for i in range(pup_count)]
        

    def heal_all(self):
        for puppy in self.pup_count:
            self.pup_count[states[2]] = []
    
    def all_are_healthy(self):
        for puppy in self.pup_count:
            if self.pup_count[states[2]]:
                return True
            else:
                return False
                
    def give_away_all(self):
        for puppie in self.pup_count:
            if self.pup_count[states[2]]:
                pup_count = 0

                
class Vet:
    
    def __init__(self, name, plant):
        self.name = name
        self.plant = plant
        
    def work(self):
        Dog.heal_all
        print('Щенки лечатся')
        
    def care(self):
       if Dog.all_are_healthy is True:
           Dog.give_away_all()
       else:
           print('Не все щенки здоровы')
                
    # def knowledge_base(self):
    #     print(self.pup_count[state])

        
        
        
        
        
        
        
        
        
        

        

dog = Dog(5)  
vet = Vet('Makanchik', dog)    
pup = Puppy('счастлив')
dog.heal_all()
vet.work()
vet.care() 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            