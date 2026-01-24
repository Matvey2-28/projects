class MyError(Exception):
    pass

def stuff(file):
    raise MyError
    
file = open('data.txt', 'w')

try:
    stuff(file)
finally:
    file.close