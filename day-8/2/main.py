# Load up the image
input_file = open("input", 'r')
input_data = input_file.read()
input_file.close()

# Test image data provided.
#input_data = "0222112222120000"

width = 25
height = 6
layer_len = width*height

n_layers = len(input_data)//(layer_len)

# Framebuffer to render into, set to transparent.
image = [2]*layer_len

# For each layer.
for idx in range(n_layers):
    offset = idx*layer_len
    # For each pixel in the layer.
    for jdx in range(layer_len):
        # If the framebuffer is still transparent, copy the layer.
        if image[jdx] == 2:
            image[jdx] = int(input_data[offset+jdx])

# Values to display for black and white.
disp = [' ', '█']
for idx in range(height):
    for jdx in range(width):
        print(disp[image[(idx*width)+jdx]], end="")
    print("")
