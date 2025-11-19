def compress(*values):
    return values

result = compress(1, 5, 7, 8, 9)
print('Compressed:', result)


def extract(value):
    print('Extracted: ', *value)
    
    
extract(result)