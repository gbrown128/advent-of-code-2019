from collections import Counter

input_file = open("input", 'r')
input_data = input_file.read()
input_file.close()

width = 25
height = 6
layer_len = width*height

n_layers = len(input_data)//(layer_len)

zeros = layer_len
result = 0

for idx in range(n_layers):
    layer = input_data[idx*layer_len:(idx+1)*layer_len]
    print(count)
    if count['0'] < zeros:
        zeros = count['0']
        result = count['1'] * count['2']

print(result)
