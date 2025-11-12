import time



timer = time.time()
symbols = 'Python'
symbol_codes = [ord(symbol) for symbol in symbols]
print(symbol_codes)

timer = time.time()
out = []
for symbol in range(len(symbols)):
    out.append(symbol)
print(time.time() - timer)

symbols = 'Snake'
symbol_codes = (ord(symbol) for symbol in symbols)
print(symbol_codes)

for object in symbol_codes:
    print(object)