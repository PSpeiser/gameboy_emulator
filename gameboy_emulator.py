from collections import namedtuple


class CPU(object):
    def __init__(self):
        class Registers(object):
            def __init__(self):
                self.a = 0
                self.b = 0
                self.c = 0
                self.d = 0
                self.e = 0
                self.h = 0
                self.l = 0
                self.f = 0
                self.pc = 0 #16 bit registers
                self.sp = 0
                self.m = 0 #clock for the last instructions
                self.t = 0
        self.registers = Registers()
        class Flags(object):
            self.cy = False
            self.z = False
            self.n = False
            self.h = False
            self.cy = False
        self.flags = Flags()

        class Clock(object):
            self.m = 0
            self.t = 0
        self.clock = Clock()

        print self.registers
        print self.flags
        print self.clock

    def clear_flags(self):
        self.flags.z = False
        self.flags.n = False
        self.flags.h = False
        self.flags.cy = False

    def ADDr(self,r):
        #need to have the name of the register here NOT the bitcode
        self.clear_flags()
        #check for half-carry
        if (getattr(self.registers,r) & 0xF) + (self.registers.a & 0xf) > 15:
            self.flags.h = True
        #add register r to register a
        self.registers.a += getattr(self.registers,r)
        #check for carry
        if self.registers.a > 255:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 1
        self.registers.t = 4

    def ADDn(self,n):
        self.clear_flags()
        #check for half-carry
        if (n & 0xF) + (self.registers.a & 0xF) > 15:
            self.flags.h = True
        #add immediate operand n to register a
        self.registers.a += n
        #check for carry
        if self.registers.a > 255:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2
        self.registers.t = 8

    def NOP(self):
        self.registers.m = 1
        self.registers.t = 4

