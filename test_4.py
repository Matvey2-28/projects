import random as rd

flowers = ['Розы', 'Пионы', 'Тюльпаны']
colors = ['красный', 'синий', 'оранжевый', 'желтый', 'зеленый']
color_random = [rd.choice(colors) for i in range(len(flowers))]

print(dict(zip(flowers, color_random)))