fio = 'MALIK MATVEY GEORGIEVICH'

fio_codes = [ord(symbol) for symbol in fio]
fio1_codes = [ord(symbol) for symbol in fio.lower()]

print(sum(fio_codes) + sum(fio1_codes))