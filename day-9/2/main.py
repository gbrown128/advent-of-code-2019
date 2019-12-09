import itertools

# First do all the input file gubbins.
input_file = open("input", 'r')
input_data = input_file.read().split(',')
input_file.close()

# String to int conversion.
for idx in range(len(input_data)):
    input_data[idx] = int(input_data[idx])

#input_data = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
#input_data = [1102,34915192,34915192,7,4,7,99,0]

class IntBox():
    """
    An incode computer implementation.

    The state variable includes the following values

    -1 = Exception raised.
    0 = Reset and ready to run.
    1 = Started (used internally)
    3 = Paused for input.
    4 = Paused for output.
    99 = Halted
    """
    def __init__(self, program):
        """ Load the program to memory and initialise """
        self.program = program.copy()
        self.reset()

    def reset(self):
        """ Reset the computer ready for a fresh run. """
        self.mem = self.program.copy()
        self.pc = 0
        self.inp = None
        self.out = None
        self.rel = 0
        self.state = 0
        return self.state

    def start(self):
        """ Reset and start running. """
        self.reset()
        self.resume()
        return self.state

    def resume(self):
        """ Continue execution after I/O halt. """
        if self.state not in [99, -1]:
            # Run until a halt occurs.
            #while not self.tick():
            #    pass
            while True:
                try:
                    result = self.tick()
                except IndexError as e:
                    print("Mem oflo: {}, extended to ".format(len(self.mem)), end="")
                    self.mem.extend([0]*100)
                    print(len(self.mem))
                    continue
                if not result == 0:
                    break
        return self.state

    def decode(self, ins):
        """ Decode an incode instruction """
        ins = str(ins)
        # Any instruction may have length 1 or two.
        if len(ins) in [1, 2]:
#            print("Decoded: {}".format((int(ins), 0, 0, 0)))
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
#        print("Decoded: {}".format((int(ins[-2:]), mode1, mode2, mode3)))
        return (int(ins[-2:]), mode1, mode2, mode3)

    def tick(self):
        """ Perform one instruction. """
#        print("Tick at PC: {}".format(self.pc))

        # Decode this instruction.
        opcode, mode1, mode2, mode3 = self.decode(self.mem[self.pc])

        # Shared operand fetch block.
        if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
            if mode1 == 1:
                op1 = self.mem[self.pc+1]
            elif mode1 == 2:
                op1 = self.mem[self.mem[self.pc+1] + self.rel]
            else:
                op1 = self.mem[self.mem[self.pc+1]]
        if opcode in [1, 2, 5, 6, 7, 8]:
            if mode2 == 1:
                op2 = self.mem[self.pc+2]
            elif mode2 == 2:
                op2 = self.mem[self.mem[self.pc+2] + self.rel]
            else:
                op2 = self.mem[self.mem[self.pc+2]]

        # When operand 1 is the output, compute the output address.
        if opcode in [3]:
            if mode3 == 1:
                print("Addressing mode 1 for output at PC: {}".format(self.pc))
            else:
                out_addr = self.mem[self.pc+1]
            if mode3 == 2:
                out_addr += self.rel

        # When operand 3 is the output, compute the output address.
        if opcode in [1,2,3,7,8]:
            if mode3 == 1:
                print("Addressing mode 1 for output at PC: {}".format(self.pc))
            else:
                out_addr = self.mem[self.pc+3]
            if mode3 == 2:
                out_addr += self.rel

        # Add / op1 op2 out
        if opcode == 1:
            self.mem[out_addr] = op1+op2
            self.pc += 4
        # Multiply / op1 op2 out
        elif opcode == 2:
            self.mem[out_addr] = op1*op2
            self.pc += 4
        # Input / out
        elif opcode == 3:
            if self.inp == None:
                # No input, hang up on this instruction and wait for it to be given.
                self.state = 3
                return 3
            self.mem[out_addr] = self.inp
            self.inp = None
            self.state = 1
            self.pc += 2
        # Output / op1
        elif opcode == 4:
            print("{:>05d}> {}".format(self.pc, op1))
            ## First pass into the instruction, set the output and halt.
            #if self.state == 1:
            #    self.out = op1
            #    self.state = 4
            #    return 4
            ## 2nd time round, clean up and resume.
            #self.out = None
            #self.state = 1
            self.pc += 2
        # Jump if true / op1 (test) op2 (jump to)
        elif opcode == 5:
            if op1:
                self.pc = op2
            else:
                self.pc += 3
        # Jump if false / op1 (test) op2 (jump to)
        elif opcode == 6:
            if not op1:
                self.pc = op2
            else:
                self.pc += 3
        # Less than / op1 (<) op2 out
        elif opcode == 7:
            if op1 < op2:
                self.mem[out_addr] = 1
            else:
                self.mem[out_addr] = 0
            self.pc += 4
        # Equals / op1 (==) op2 out
        elif opcode == 8:
            if op1 == op2:
                self.mem[out_addr] = 1
            else:
                self.mem[out_addr] = 0
            self.pc += 4
        # Relative base adjust
        elif opcode == 9:
            self.rel += op1
            self.pc += 2
        # Halt / -
        elif opcode == 99:
            print("Halt at PC: {}!".format(self.pc))
#            print(self.mem[0])
#            print(self.mem)
            self.state = 99
            return 99
        else:
            self.state = -1
            print("Invalid Instruction!")
            return -1
        return 0


box = IntBox(input_data)
# Run and add hit input 1.
box.start()
box.inp = 2
box.resume()
