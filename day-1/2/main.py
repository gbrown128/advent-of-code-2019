from math import floor

input_file = open("input", "r")
input_data = input_file.read()

total = 0

def get_fuel(mass):
    mass /= 3
    mass = floor(mass)
    mass -= 2
    if mass < 9:
        return mass
    else:
        return mass + get_fuel(mass)

for module in input_data.split('\n'):
    try:
        module = int(module)
    except ValueError:
        continue
    total += get_fuel(module)

print(total)
