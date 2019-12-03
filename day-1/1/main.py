from math import floor

input_file = open("input", "r")
input_data = input_file.read()

total = 0

for module in input_data.split('\n'):
    print(module)
    try:
        module = int(module)
    except ValueError:
        continue
    module /= 3
    module = floor(module)
    module -= 2
    total += module

print(total)
