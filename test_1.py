class Buisnessman:
    def_age = 22
    def_name = 'Mihail Galustyan'    
    
    def __init__(self, age=def_age, name=def_name, money = 99999999, business = 'Есть'):
        self.age = age
        self.name = name
        self._money = money
        self._business = business
    
    
    def info(self):
        print(f'Имя: {self.name}')
        print(f'Возраст: {self.age}')
        print(f'Каптиал: {self._money}')
        print(f'Наличие бизнеса: {self._business}')
        
    @classmethod
    def def_info(cls):
        print('----Имя-и-возраст-предпринимателя----')
        print(f'{cls.def_age}')
        print(f'{cls.def_name}')
        
        
    @staticmethod
    def buy_business(self):
        if self._money >= self._price - Business.final_price():
            self._money -= self._price - Business.final_price()
            print(f'{self.name} приобрел бизнес стоимостью {self._price} руб')
        else:
            print(f'У {self.name} недостаточно средств на покупку данного бизнеса')
    
    
    def earn_money(self):
        self._money += 200000
        

class Business:
    
    def __init__(self, area=67000000, price=10000000):
        self._area = area
        self._price = price
        
    @property    
    def final_price(self, sale):
        self.sale = sale
        self.final_price -= self._price // self.sale
        return self.final_price
    
class RestarauntBusiness(Business):
    
    def __init__(self, salary=50000000):
        super.__init__(area=50000000, price=20000000)
        self.salary = salary
        
restoran = RestarauntBusiness()    
bisnes = Business()  
man = Buisnessman()   
man.info()
Buisnessman.def_info()
bisnes.final_price
Buisnessman.buy_business()
