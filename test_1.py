def logger(filename):
    def decorator(num_1):
        def wrapper(*args, **kwargs):
            result = num_1(*args, **kwargs)
            f = open(filename, 'w')
            f.write(str(result))
            f.close()
            return result
        return wrapper 
    return decorator 

@logger('file_test_1.txt')
def summator(num_2):
    return sum(num_1, num_2)

summator(3)