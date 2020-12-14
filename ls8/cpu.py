"""CPU functionality."""

import sys

#ALU ops

ADD = 0b10100000 
SUB = 0b10100001 
MUL = 0b10100010 
DIV = 0b10100011 

CMP = 0b10100111 

#PC mutators

JMP = 0b01010100 
JEQ = 0b01010101 
JNE = 0b01010110 

#Other

HLT = 0b00000001 

LDI = 0b10000010

PRN = 0b01000111

#Flags
EQUAL = 0b001
GREATER_THAN = 0b010
LESS_THAN = 0b100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.flag = 0
        self.running = True
        self.branch_table = {
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            0b10100011: self.DIV,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN
        }

    def HLT(self):
        print("HLT")
        print(self.pc)
        self.pc +=1
        self.running = False
        sys.exit()


    def LDI(self):
        print("LDI")
        print(self.pc)
        index = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.pc += 3


    def PRN(self):
        print("PRN")
        print(self.pc)
        index = self.ram_read(self.pc + 1)
        print(self.reg[index])

        self.pc += 2


    def ADD(self):
        print("ADD")
        print(self.pc)
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2= self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = num_1 + num_2
        self.pc += 3


    def SUB(self):
        print("SUB")
        print(self.pc)
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = num_1 - num_2
        self.pc+=3


    def MUL(self):
        print("MUL")
        print(self.pc)
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = num_1 * num_2
        self.pc += 3


    def DIV(self):
        print("DIV")
        print(self.pc)
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = num_1 // num_2
        self.pc += 3


    def CMP(self):
        print("CMP")
        print(self.pc)
        reg_1 = self.reg[self.ram_read(self.pc + 1)]
        reg_2 = self.reg[self.ram_read(self.pc + 2)]

        if reg_1 > reg_2:
            self.flag = GREATER_THAN

        elif reg_1 < reg_2:
            self.flag = LESS_THAN

        else:
            self.flag = EQUAL

        self.pc += 3

# JEQ
# 12
# ldi 0


    def JMP(self):
        print("JMP")
        print(self.pc)
        jump = self.reg[self.ram_read(self.pc + 1)]
        self.pc = jump


    def JEQ(self):
        print("JEQ")
        print(self.pc)
        if self.flag == EQUAL:
            self.pc = self.reg[self.ram_read(self.pc + 1)]

        else:
            self.pc += 2


    def JNE(self):
        print("JNE")
        print(self.pc)
        if self.flag != EQUAL:
            self.pc = self.reg[self.ram_read(self.pc + 1)]

        else:
            self.pc += 2
    

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR


    def load(self):
        """Load a program into memory."""
        try:
            print(sys.argv)

            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}: missing filename argument')
                print(f'Usage: python3 {sys.argv[0]} <somefilename>')
                sys.exit(1)

            # add a counter that adds to memory at that index
            ram_index = 0

            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split("#", 1)[0]
                    stripped_split_line = split_line.strip()

                    if stripped_split_line != "":
                        command = int(stripped_split_line, 2)
            
                        # load command into memory
                        self.ram[ram_index] = command
                        ram_index += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")


        # address = 0
        

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] > self.reg[reg_b]:
                self.flag = GREATER_THAN
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.flag = LESS_THAN
            else:
                self.flag = EQUAL
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        """
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
        """

        while self.running:
            IR = self.ram[self.pc]

            if IR in self.branch_table:
                self.branch_table[IR]()



