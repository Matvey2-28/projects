fio = 'MALIK MATVEY GEORGIEVICH'
fio1 = 'malik matvey georgievich'

fio_codes = [ord(symbol) for symbol in fio]
fio1_codes = [ord(symbol) for symbol in fio1]

print(sum(fio_codes) + sum(fio1_codes))