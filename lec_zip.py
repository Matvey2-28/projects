names = ['John', 'David', 'Maria', 'Richard']
ages = [16, 25, 19, 41]
isTeenager = [True, False, True, False]

users = list(zip(names, ages, isTeenager))
print(users)

print('User age:', dict(zip(names, ages)))

def checker(user):
    name, age = user
    return age > 21


users = list(zip(names, ages))
canDrinkAlcohol = list(filter(checker, users))
print(canDrinkAlcohol)