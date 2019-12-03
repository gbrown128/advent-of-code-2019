input_file = open("input", "r")
input_data = input_file.read().split('\n')
wire1 = input_data[0].split(',')
wire2 = input_data[1].split(',')

#wire1 = ['R8','U5','L5','D3']
#wire2 = ['U7','R6','D4','L4']

#wire1 = ["R75","D30","R83","U83","L12","D49","R71","U7","L72"]
#wire2 = ["U62","R66","U55","R34","D71","R55","D58","R83"]

#wire1 = ["R98","U47","R26","D63","R33","U87","L62","D20","R33","U53","R51"]
#wire2 = ["U98","R91","D20","R16","D67","R40","U7","R15","U6","R7"]

"""
Intersection detection algorithm.

My plan is to break each wire into its component lines.
Each line entry will have:
    Direction, horizontal/vertical
    The line's X or Y position
    The lines start and end position on the complimentary axis.

Perpendicular line segments between data sets will be tested and
crossings identified. Manhattan distances will then be stored.
"""

# Note the convention that the X axis is 0, Y axis is 1
directions = {'L': (0, -1), 'R': (0, +1), 'U': (1, +1), 'D': (1, -1)}

# Generate datasets for the wires
w1d = []
pos = [0, 0]
for instruction in wire1:
    # Split the instruction to its parts.
    direction = instruction[0]
    length = int(instruction[1:])
    # Convert that to the axis, and the sign of the direction along the axis
    ax, sign = directions[direction]
    # Compute the start and end points along the axis.
    start = pos[ax]
    end = start + length*sign

    # Create the entry for the intersection finding algorithm.
    w1d.append([ax, pos[1-ax], min(start, end), max(start, end)])
    # Update the current position for the start of the next line
    pos[ax] = end

print("Wrire one done, ends at {}, with {} segments".format(pos, len(w1d)))

# Repeat above for line 2
w2d = []
pos = [0, 0]
for instruction in wire2:
    direction = instruction[0]
    ax, sign = directions[direction]
    length = int(instruction[1:])
    start = pos[ax]
    end = start + length*sign

    w2d.append([ax, pos[1-ax], min(start, end), max(start, end)])
    pos[ax] = end

print("Wrire two done, ends at {}, with {} segments".format(pos, len(w2d)))

intercepts = []

# Now find the crossings.
for seg1 in w1d:
    for seg2 in w2d:
        # Only need to find crossings on perpendicular lines.
        if not seg1[0] == seg2[0]:
            if seg2[1] in range(seg1[2], seg1[3]):
                if seg1[1] in range(seg2[2], seg2[3]):
                    # Intercept detected.
                    intercepts.append(abs(seg1[1])+abs(seg2[1]))

# This system successfully idenfities the zero intercept.
# Remove that result.
del intercepts[0]

print(min(intercepts))
