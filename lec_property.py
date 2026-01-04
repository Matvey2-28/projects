class SummatorClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    @property
    def sum_two_num(self):
        print(f'Сумма двух чисел равна {self.a + self.b}')
        
sum_cls = SummatorClass(1, 2)
sum_cls.sum_two_num