# This project essentially requires us to plot the orbital tree
# and then count the number of steps needed to reach the COM from
# every point in the tree.

# Starting data looks a bit like a dict, so we'll start by converting
# it into dict format.
# Input data is given as key) value

input_file = open("input", 'r')
input_data = input_file.read()
input_file.close()

kv_pairs = input_data.split('\n')

tree = {}

# Load up the diict.
# Key = outer object
# Value = inner object
for pair in kv_pairs:
    try:
        value, key = pair.split(')')
        tree[key] = value
    except ValueError:
        pass

orbits = 0

for inner, outer in tree.items():
    print("=======")
    while True:
        print(inner)
        if inner == "COM":
            break
        outer = inner
        inner = tree[outer]
        orbits += 1

print(orbits)
