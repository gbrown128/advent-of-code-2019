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

# Plot the orbit tree for YOU and SAN into memory.
outer = "YOU"
inner = tree[outer]
my_tree = [outer]
while True:
    my_tree.append(inner)
    if inner == "COM":
        break
    outer = inner
    inner = tree[outer]

outer = "SAN"
inner = tree[outer]
santa_tree = [outer]
while True:
    santa_tree.append(inner)
    if inner in my_tree:
        break
    outer = inner
    inner = tree[outer]

# Truncate my list where it collides with Santas
first_common = santa_tree[-1]
idx = my_tree.index(first_common)

my_tree = my_tree[0:idx]

print(my_tree)
print(santa_tree)

# -3 since to convert from number of objects to hop count, and hop to one before santa!
hops = len(my_tree) + len(santa_tree) - 3

print(hops)
