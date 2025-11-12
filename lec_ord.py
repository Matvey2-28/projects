text = "Hello"

for symbol in text:
    print(ord(symbol), end = "; ")
print()

codes = [119, 111, 114, 108, 100]
symbols = ""

for code in codes:
    symbols += chr(code)
    
print(symbols)

print(chr(11111))