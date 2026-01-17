lambda_list = [lambda x: x + 1,
               lambda x: x * 2,
               lambda x: x ** 3]
for i in lambda_list:
    print(i(2))

print(lambda_list[0](4))