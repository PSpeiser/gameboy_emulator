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

    def ADDr(self, r):
        #need to have the name of the register here NOT the bitcode
        self.clear_flags()
        #check for half-carry
        if (getattr(self.registers, r) & 0xF) + (self.registers.a & 0xf) > 15:
            self.flags.h = True
            #add register r to register a
        self.registers.a += getattr(self.registers, r)
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

    def ADDn(self, n):
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


class MMU(object):
    inbios = True

    def __init__(self,gpu):
        self.bios = [0x31, 0xFE, 0xFF, 0xAF, 0x21, 0xFF, 0x9F, 0x32, 0xCB, 0x7C, 0x20, 0xFB, 0x21, 0x26, 0xFF, 0x0E,
                     0x11, 0x3E, 0x80, 0x32, 0xE2, 0x0C, 0x3E, 0xF3, 0xE2, 0x32, 0x3E, 0x77, 0x77, 0x3E, 0xFC, 0xE0,
                     0x47, 0x11, 0x04, 0x01, 0x21, 0x10, 0x80, 0x1A, 0xCD, 0x95, 0x00, 0xCD, 0x96, 0x00, 0x13, 0x7B,
                     0xFE, 0x34, 0x20, 0xF3, 0x11, 0xD8, 0x00, 0x06, 0x08, 0x1A, 0x13, 0x22, 0x23, 0x05, 0x20, 0xF9,
                     0x3E, 0x19, 0xEA, 0x10, 0x99, 0x21, 0x2F, 0x99, 0x0E, 0x0C, 0x3D, 0x28, 0x08, 0x32, 0x0D, 0x20,
                     0xF9, 0x2E, 0x0F, 0x18, 0xF3, 0x67, 0x3E, 0x64, 0x57, 0xE0, 0x42, 0x3E, 0x91, 0xE0, 0x40, 0x04,
                     0x1E, 0x02, 0x0E, 0x0C, 0xF0, 0x44, 0xFE, 0x90, 0x20, 0xFA, 0x0D, 0x20, 0xF7, 0x1D, 0x20, 0xF2,
                     0x0E, 0x13, 0x24, 0x7C, 0x1E, 0x83, 0xFE, 0x62, 0x28, 0x06, 0x1E, 0xC1, 0xFE, 0x64, 0x20, 0x06,
                     0x7B, 0xE2, 0x0C, 0x3E, 0x87, 0xF2, 0xF0, 0x42, 0x90, 0xE0, 0x42, 0x15, 0x20, 0xD2, 0x05, 0x20,
                     0x4F, 0x16, 0x20, 0x18, 0xCB, 0x4F, 0x06, 0x04, 0xC5, 0xCB, 0x11, 0x17, 0xC1, 0xCB, 0x11, 0x17,
                     0x05, 0x20, 0xF5, 0x22, 0x23, 0x22, 0x23, 0xC9, 0xCE, 0xED, 0x66, 0x66, 0xCC, 0x0D, 0x00, 0x0B,
                     0x03, 0x73, 0x00, 0x83, 0x00, 0x0C, 0x00, 0x0D, 0x00, 0x08, 0x11, 0x1F, 0x88, 0x89, 0x00, 0x0E,
                     0xDC, 0xCC, 0x6E, 0xE6, 0xDD, 0xDD, 0xD9, 0x99, 0xBB, 0xBB, 0x67, 0x63, 0x6E, 0x0E, 0xEC, 0xCC,
                     0xDD, 0xDC, 0x99, 0x9F, 0xBB, 0xB9, 0x33, 0x3E, 0x3c, 0x42, 0xB9, 0xA5, 0xB9, 0xA5, 0x42, 0x4C,
                     0x21, 0x04, 0x01, 0x11, 0xA8, 0x00, 0x1A, 0x13, 0xBE, 0x20, 0xFE, 0x23, 0x7D, 0xFE, 0x34, 0x20,
                     0xF5, 0x06, 0x19, 0x78, 0x86, 0x23, 0x05, 0x20, 0xFB, 0x86, 0x20, 0xFE, 0x3E, 0x01, 0xE0, 0x50]
        self.rom = []
        self.wram = []
        self.eram = []
        self.zram = []
        self.gpu = gpu

    def read_byte(self, addr):
        if addr < 0x1000:
            if self.inbios:
                if addr < 0x0100:
                    return self.bios[addr]
            return self.rom[addr]
        #Rom 0
        elif 0x1000 >= addr < 0x4000:
            return self.rom[addr]
        #Rom 1
        elif 0x4000 >= addr < 0x8000:
            return self.rom[addr]
        #VRAM
        elif 0x8000 >= addr < 0xA000:
            return self.gpu.vram[addr & 0x1FFF]

        #External RAM 8k
        elif 0xA000 >= addr < 0xC000:
            return self.eram[addr & 0x1FFF]

        #Working Ram 8k
        elif 0xC000 >= addr < 0xE000:
            return self.wram[addr & 0x1FFF]

        #working ram shadow
        elif 0xE000 >= addr < 0xF000:
            return self.wram[addr & 0x1FFF]

        #working ram shadow, I/O, zero page ram
        elif addr >= 0xF000:
            area = addr & 0x0F00
            if area < 0xE00:
                return self.wram[addr & 0x1FFF]
            elif area == 0xE00:
                if addr < 0xFEA0:
                    return self.gpu.oam[addr & 0xFF]
                else:
                    return 0
            elif area == 0xF00:
                if addr >= 0xFF80:
                    return self.zram[addr & 0x7F]
                else:
                    #I/O Control handling happens here
                    #Currently unhandled
                    return 0

    def read_word(self, addr):
        return self.read_byte(addr) + (self.read_byte(addr + 1) << 8)

    def write_byte(self, addr, value):
        if addr < 0x1000:
            if self.inbios:
                if addr < 0x0100:
                    self.bios[addr] = value
            self.rom[addr] = value
        #Rom 0
        elif 0x1000 >= addr < 0x4000:
            self.rom[addr] = value
        #Rom 1
        elif 0x4000 >= addr < 0x8000:
            self.rom[addr] = value
        #VRAM
        elif 0x8000 >= addr < 0xA000:
            self.gpu.vram[addr & 0x1FFF] = value

        #External RAM 8k
        elif 0xA000 >= addr < 0xC000:
            self.eram[addr & 0x1FFF] = value

        #Working Ram 8k
        elif 0xC000 >= addr < 0xE000:
            self.wram[addr & 0x1FFF] = value

        #working ram shadow
        elif 0xE000 >= addr < 0xF000:
            self.wram[addr & 0x1FFF] = value

        #working ram shadow, I/O, zero page ram
        elif addr >= 0xF000:
            area = addr & 0x0F00
            if area < 0xE00:
                self.wram[addr & 0x1FFF] = value
            elif area == 0xE00:
                if addr < 0xFEA0:
                    self.gpu.oam[addr & 0xFF] = value
                else:
                    raise Exception()
            elif area == 0xF00:
                if addr >= 0xFF80:
                    self.zram[addr & 0x7F] = value
                else:
                    #I/O Control handling happens here
                    #Currently unhandled
                    raise NotImplementedError()

    def write_word(self,addr,value):
        self.write_byte(addr,value & 255)
        self.write_byte(addr+1,value >> 8)

    def load(self,filename):
        f = open(filename,"rb")
        self.rom = f.read()
        return True



class GPU(object):
    def __init__(self):
        self.vram = []
        self.oam = []


cpu = CPU()
gpu = GPU()
mmu = MMU(gpu)

