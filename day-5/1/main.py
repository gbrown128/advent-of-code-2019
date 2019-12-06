input_file = open("input", 'r')
input_data = input_file.read().split(',')
input_file.close()

for idx in range(len(input_data)):
    input_data[idx] = int(input_data[idx])

pc = 0
mem = input_data

def get_input():
    global pc, mem
    return int(input("{:>05d}< ".format(pc)))

def output(out):
    global pc, mem
    print("{:>05d}> {}".format(pc, out))

def decode(ins):
    ins = str(ins)
    # Any instruction may have length 1 or two.
    if len(ins) in [1, 2]:
        return (int(ins), 0, 0, 0)
    # Otherwise it definitely has at least one mode.
    mode1 = int(ins[-3])
    try:
        mode2 = int(ins[-4])
    except IndexError:
        mode2 = 0
    try:
        mode3 = int(ins[-5])
    except IndexError:
        mode3 = 0
    return (int(ins[-2:]), mode1, mode2, mode3)

# Main program loop.
def tick():
    global pc, mem
    # Decode this instruction.
    opcode, mode1, mode2, mode3 = decode(mem[pc])

    # Shared operand fetch block. Has the potential to overflow for output!
    if opcode in [1, 2, 4]:
        if mode1 == 1:
            op1 = mem[pc+1]
        else:
            op1 = mem[mem[pc+1]]
    if opcode in [1,2]:
        if mode2 == 1:
            op2 = mem[pc+2]
        else:
            op2 = mem[mem[pc+2]]
# Not used by any instruction yet!
#        if mode3 == 1:
#            op3 = mem[pc+3]
#        else:
#            op3 = mem[mem[pc+3]]

    # Add / op1 op2 out
    if opcode == 1:
        mem[mem[pc+3]] = op1+op2
        pc += 4
    # Multiply / op1 op2 out
    elif opcode == 2:
        mem[mem[pc+3]] = op1*op2
        pc += 4
    # Input / out
    elif opcode == 3:
        mem[mem[pc+1]] = get_input()
        pc += 2
    # Output / op1
    elif opcode == 4:
        output(op1)
        pc += 2
    # Halt / -
    elif opcode == 99:
        print("Halt at PC: {}!".format(pc))
        print(mem[0])
        print(mem)
        return 0
    else:
        raise ValueError("Invalid Instruction!")
    return 1


while tick():
    pass
