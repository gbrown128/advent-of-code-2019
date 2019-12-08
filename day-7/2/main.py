import itertools

# First do all the input file gubbins.
input_file = open("input", 'r')
input_data = input_file.read().split(',')
input_file.close()

# String to int conversion.
for idx in range(len(input_data)):
    input_data[idx] = int(input_data[idx])

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
            # Run until a halt occurs..
            while not self.tick():
                pass
        return self.state

    def decode(self, ins):
        """ Decode an incode instruction """
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

    def tick(self):
        """ Perform one instruction. """
        # Decode this instruction.
        opcode, mode1, mode2, mode3 = self.decode(self.mem[self.pc])

        # Shared operand fetch block. Has the potential to overflow for output!
        if opcode in [1, 2, 4, 5, 6, 7, 8]:
            if mode1 == 1:
                op1 = self.mem[self.pc+1]
            else:
                op1 = self.mem[self.mem[self.pc+1]]
        if opcode in [1,2, 5, 6, 7, 8]:
            if mode2 == 1:
                op2 = self.mem[self.pc+2]
            else:
                op2 = self.mem[self.mem[self.pc+2]]
        # Only an output in all instructions so far!
        #if opcode in []:
        #    if mode3 == 1:
        #        op3 = self.mem[self.pc+3]
        #    else:
        #        op3 = self.mem[self.mem[self.pc+3]]

        # Add / op1 op2 out
        if opcode == 1:
            self.mem[self.mem[self.pc+3]] = op1+op2
            self.pc += 4
        # Multiply / op1 op2 out
        elif opcode == 2:
            self.mem[self.mem[self.pc+3]] = op1*op2
            self.pc += 4
        # Input / out
        elif opcode == 3:
            if self.inp == None:
                # No input, hang up on this instruction and wait for it to be given.
                self.state = 3
                return 3
            self.mem[self.mem[self.pc+1]] = self.inp
            self.inp = None
            self.state = 1
            self.pc += 2
        # Output / op1
        elif opcode == 4:
            # First pass into the instruction, set the output and halt.
            if self.state == 1:
                self.out = op1
                self.state = 4
                return 4
            # 2nd time round, clean up and resume.
            self.out = None
            self.state = 1
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
                self.mem[self.mem[self.pc+3]] = 1
            else:
                self.mem[self.mem[self.pc+3]] = 0
            self.pc += 4
        # Equals / op1 (==) op2 out
        elif opcode == 8:
            if op1 == op2:
                self.mem[self.mem[self.pc+3]] = 1
            else:
                self.mem[self.mem[self.pc+3]] = 0
            self.pc += 4
        # Halt / -
        elif opcode == 99:
            #print("Halt at PC: {}!".format(self.pc))
            #print(self.mem[0])
            #print(self.mem)
            self.state = 99
            return 99
        else:
            self.state = -1
            print("Invalid Instruction!")
            return -1
        return 0

# Generate the amplifiers.
amps = []
for idx in range(5):
    amps.append(IntBox(input_data))

# Generate all the permutations of the phase settings.
settings = list(itertools.permutations(range(5, 10)))

max = 0

# For each possible phasing setup.
for setting in settings:
    # Reset all the amplifiers, load the new phase settings.
    for idx in range(len(amps)):
        amps[idx].start()
        amps[idx].inp = setting[idx]
        amps[idx].resume()
    # Loop through the feedback path until done.
    signal = 0
    while not amps[4].state == 99:
        for amp in amps:
            amp.inp = signal
            amp.resume()
            signal = amp.out
            amp.resume()
    print(signal)
    if signal > max:
        max = signal

print("Done! Result: {}".format(max))
