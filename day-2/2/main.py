# Load the program in:
input_file = open("input", "r")
input_data = input_file.read()
input_file.close()
input_program = input_data.split(',')

import time

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
    # Return the program result.
    return mem[0]

def main():
    global mem, pc
    print("Run noun search")
    # Looks like the noun increments the result in large steps.
    result = 0
    noun = 0
    while result < 19690720:
        mem = input_program.copy()
        pc = 0
        mem[1] = noun
        result = run()
        noun += 1
    noun -= 2
    print("Got noun: {}".format(noun))
    print("Run verb search")
    # At this point it seems verb is added to the result at the end
    # But we'll run the search since I have copy paste!
    result = 0
    verb = 0
    while result < 19690720:
        mem = input_program.copy()
        pc = 0
        mem[1] = noun
        mem[2] = verb
        result = run()
        verb += 1
    verb -= 1
    print(result)
    print("Got verb: {}, result: {}{}".format(verb, noun, verb))

    

main()
