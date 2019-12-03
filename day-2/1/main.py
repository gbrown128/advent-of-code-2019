test1 = [1,0,0,0,99]
test2 = [2,3,0,3,99]
test3 = [2,4,4,5,99,0]
test4 = [1,1,1,4,99,5,6,0,99]

# Load the program in:
input_file = open("input", "r")
input_data = input_file.read()
input_file.close()
input_program = input_data.split(',')

for idx in range(len(input_program)):
    input_program[idx] = int(input_program[idx])

def compute():
    global pc, mem
    """ Run the intcode program to completion. """
    while True:
        try:
            # Add
            if mem[pc] == 1:
                # Operand Fetch
                o1 = mem[mem[pc+1]]
                o2 = mem[mem[pc+2]]
                # Write Result
                mem[mem[pc+3]] = o1+o2
            # Multiply
            elif mem[pc] == 2:
                # Operand Fetch
                o1 = mem[mem[pc+1]]
                o2 = mem[mem[pc+2]]
                # Write Result
                mem[mem[pc+3]] = o1*o2
            # Halt
            elif mem[pc] == 99:
                break
            else:
                print("[ERROR: Invalid Opcode {}]".format(mem[pc]))
                break
            # Increment PC
            pc += 4
        # Expand memory as required by the program.
        except IndexError:
            print("Expanding memory for PC: {}".format(pc))
            mem.extend([0]*(pc))
            continue

def run():
    global pc, mem
    """ Start computation, print result. """
    compute()
    print("Result: {}".format(mem[0]))
    print("PC    : {}".format(pc))
    print("System State:")
    print(mem)

mem = test1
pc = 0
run()
mem = test2
pc = 0
run()
mem = test3
pc = 0
run()
mem = test4
pc = 0
run()
mem = input_program
print(mem)
pc = 0
run()
