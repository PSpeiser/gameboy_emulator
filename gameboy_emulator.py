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

        self.registers = Registers()

        class Flags(object):
            def __init__(self):
                self.z = False
                self.n = False
                self.h = False
                self.cy = False

        self.flags = Flags()

        class Clock(object):
            self.m = 0

        self.clock = Clock()

    #region Utility functions

    def get_hl_value(self):
        hladdr = (self.registers.h << 8) + self.registers.l
        hlval = mmu.read_byte(hladdr)
        return hlval

    def clear_flags(self):
        self.flags.z = False
        self.flags.n = False
        self.flags.h = False
        self.flags.cy = False


    #endregion

    #region 8-Bit Transfer and Input/Output Instructions
    def LDr_r(self,r,r2):
        setattr(self.registers,r,getattr(self.registers,r2))
        self.registers.m = 1
    #region LDr_r Shortcuts
    def LDa_a(self):
        self.LDr_r('a','a')
    def LDa_b(self):
        self.LDr_r('a','b')
    def LDa_c(self):
        self.LDr_r('a','c')
    def LDa_d(self):
        self.LDr_r('a','d')
    def LDa_e(self):
        self.LDr_r('a','e')
    def LDa_h(self):
        self.LDr_r('a','h')
    def LDa_l(self):
        self.LDr_r('a','l')
    def LDb_a(self):
        self.LDr_r('b','a')
    def LDb_b(self):
        self.LDr_r('b','b')
    def LDb_c(self):
        self.LDr_r('b','c')
    def LDb_d(self):
        self.LDr_r('b','d')
    def LDb_e(self):
        self.LDr_r('b','e')
    def LDb_h(self):
        self.LDr_r('b','h')
    def LDb_l(self):
        self.LDr_r('b','l')
    def LDc_a(self):
        self.LDr_r('c','a')
    def LDc_b(self):
        self.LDr_r('c','b')
    def LDc_c(self):
        self.LDr_r('c','c')
    def LDc_d(self):
        self.LDr_r('c','d')
    def LDc_e(self):
        self.LDr_r('c','e')
    def LDc_h(self):
        self.LDr_r('c','h')
    def LDc_l(self):
        self.LDr_r('c','l')
    def LDd_a(self):
        self.LDr_r('d','a')
    def LDd_b(self):
        self.LDr_r('d','b')
    def LDd_c(self):
        self.LDr_r('d','c')
    def LDd_d(self):
        self.LDr_r('d','d')
    def LDd_e(self):
        self.LDr_r('d','e')
    def LDd_h(self):
        self.LDr_r('d','h')
    def LDd_l(self):
        self.LDr_r('d','l')
    def LDe_a(self):
        self.LDr_r('e','a')
    def LDe_b(self):
        self.LDr_r('e','b')
    def LDe_c(self):
        self.LDr_r('e','c')
    def LDe_d(self):
        self.LDr_r('e','d')
    def LDe_e(self):
        self.LDr_r('e','e')
    def LDe_h(self):
        self.LDr_r('e','h')
    def LDe_l(self):
        self.LDr_r('e','l')
    def LDh_a(self):
        self.LDr_r('h','a')
    def LDh_b(self):
        self.LDr_r('h','b')
    def LDh_c(self):
        self.LDr_r('h','c')
    def LDh_d(self):
        self.LDr_r('h','d')
    def LDh_e(self):
        self.LDr_r('h','e')
    def LDh_h(self):
        self.LDr_r('h','h')
    def LDh_l(self):
        self.LDr_r('h','l')
    def LDl_a(self):
        self.LDr_r('l','a')
    def LDl_b(self):
        self.LDr_r('l','b')
    def LDl_c(self):
        self.LDr_r('l','c')
    def LDl_d(self):
        self.LDr_r('l','d')
    def LDl_e(self):
        self.LDr_r('l','e')
    def LDl_h(self):
        self.LDr_r('l','h')
    def LDl_l(self):
        self.LDr_r('l','l')
    #endregion

    def LDr_n(self,r):
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        setattr(self.registers,r,n)
        self.registers.m = 2
    #region LDr_n Shortcuts
    def LDa_n(self):
        self.LDr_n('a')
    def LDb_n(self):
        self.LDr_n('b')
    def LDc_n(self):
        self.LDr_n('c')
    def LDd_n(self):
        self.LDr_n('d')
    def LDe_n(self):
        self.LDr_n('e')
    def LDh_n(self):
        self.LDr_n('h')
    def LDl_n(self):
        self.LDr_n('l')
    #endregion

    def LDr_hl(self,r):
        addr = (self.registers.h << 8) + self.registers.l
        value = mmu.read_byte(addr)
        setattr(self.registers,r,value)
        self.registers.m = 2
    #region LDr_hl Shortcuts
    def LDa_hl(self):
        self.LDr_hl('a')
    def LDb_hl(self):
        self.LDr_hl('b')
    def LDc_hl(self):
        self.LDr_hl('c')
    def LDd_hl(self):
        self.LDr_hl('d')
    def LDe_hl(self):
        self.LDr_hl('e')
    def LDh_hl(self):
        self.LDr_hl('h')
    def LDl_hl(self):
        self.LDr_hl('l')
    #endregion


    def LDhl_r(self,r):
        addr = (self.registers.h << 8) + self.registers.l
        value = getattr(self.registers,r)
        mmu.write_byte(addr,value)
        self.registers.m = 2
    #region LDhl_r
    def LDhl_a(self):
        self.LDhl_r('a')
    def LDhl_b(self):
        self.LDhl_r('b')
    def LDhl_c(self):
        self.LDhl_r('c')
    def LDhl_d(self):
        self.LDhl_r('d')
    def LDhl_e(self):
        self.LDhl_r('e')
    def LDhl_h(self):
        self.LDhl_r('h')
    def LDhl_l(self):
        self.LDhl_r('l')
    #endregion

    def LDhl_n(self):
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        addr = (self.registers.h << 8) + self.registers.l
        mmu.write_byte(addr,n)
        self.registers.m = 3

    def LDa_bc(self):
        addr = (self.registers.b << 8) + self.registers.c
        value = mmu.read_byte(addr)
        self.registers.a = value
        self.registers.m = 2

    def LDa_de(self):
        addr = (self.registers.d << 8) + self.registers.e
        value = mmu.read_byte(addr)
        self.registers.a = value
        self.registers.m = 2

    def LDa_c(self):
        addr = 0xFF00 + self.registers.c
        value = mmu.read_byte(addr)
        self.registers.a = value
        self.registers.m = 2

    def LDc_a(self):
        addr = 0xFF00 + self.registers.c
        mmu.write_byte(addr,self.registers.a)
        self.registers.m = 2

    def LDa_n(self):
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = mmu.read_byte(0xFF00 + n)
        self.registers.m = 3

    def LDn_a(self):
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        mmu.write_byte(n,self.registers.a)
        self.registers.m = 3

    def LDa_nn(self):
        n = mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.a = mmu.read_byte(n)
        self.registers.m = 4

    def LDnn_a(self):
        n = mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        mmu.write_byte(n,self.registers.a)
        self.registers.m = 4

    def LDa_hli(self):
        addr = (self.registers.h << 8) + self.registers.l
        self.registers.a = mmu.read_byte(addr)
        #increment hl
        addr += 1
        self.registers.h = (addr >> 8) & 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDa_hld(self):
        addr = (self.registers.h << 8) + self.registers.l
        self.registers.a = mmu.read_byte(addr)
        #decrement hl
        addr -= 1
        self.registers.h = (addr >> 8)& 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDbc_a(self):
        addr = (self.registers.b << 8) + self.registers.c
        mmu.write_byte(addr,self.registers.a)
        self.registers.m = 2

    def LDde_a(self):
        addr = (self.registers.d << 8) + self.registers.e
        mmu.write_byte(addr,self.registers.a)
        self.registers.m = 2

    def LDhli_a(self):
        addr = (self.registers.h << 8) + self.registers.l
        mmu.write_byte(addr,self.registers.a)
        #increment hl
        addr += 1
        self.registers.h = (addr >> 8) & 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDhld_a(self):
        addr = (self.registers.h << 8) + self.registers.l
        mmu.write_byte(addr,self.registers.a)
        #decrement hl
        addr -= 1
        self.registers.h = addr >> 8
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    #endregion

    #region 16-Bit Transfer Instructions
    def LDdd_nn(self,dd):
        nn = mmu.read_word(self.registers.pc)
        if dd == 'bc':
            self.registers.b = nn >> 8
            self.registers.c = nn & 0xFF
        elif dd == 'de':
            self.registers.d = nn >> 8
            self.registers.e = nn & 0xFF
        elif dd == 'hl':
            self.registers.h = nn >> 8
            self.registers.l = nn & 0xFF
        elif dd == 'sp':
            self.registers.sp = nn
        self.registers.pc += 2
        self.registers.m = 3

    #region LDdd_nn Shortcuts
    def LDbc_nn(self):
        self.LDdd_nn('bc')
    def LDde_nn(self):
        self.LDdd_nn('de')
    def LDhl_nn(self):
        self.LDdd_nn('hl')
    def LDsp_nn(self):
        self.LDdd_nn('sp')
    #endregion


    def LDsp_hl(self):
        self.registers.sp = (self.registers.h << 8) + self.registers.l
        self.registers.m = 2

    def PUSH_qq(self,qq):
        if qq == 'bc':
            qqH = self.registers.b
            qqL = self.registers.c
        elif qq == 'de':
            qqH = self.registers.d
            qqL = self.registers.e
        elif qq == 'hl':
            qqH = self.registers.h
            qqL = self.registers.l
        elif qq =='af':
            qqH = self.registers.a
            qqL = self.registers.f
        mmu.write_byte(self.registers.sp - 1,qqH)
        mmu.write_byte(self.registers.sp - 2,qqL)
        self.registers.sp -= 2
        self.registers.m = 4

    #region PUSH Shortcuts
    def PUSH_bc(self):
        self.PUSH_qq('bc')
    def PUSH_de(self):
        self.PUSH_qq('de')
    def PUSH_hl(self):
        self.PUSH_qq('hl')
    def PUSH_af(self):
        self.PUSH_qq('af')
    #endregion

    def POP_qq(self,qq):
        qqLval = mmu.read_byte(self.registers.sp)
        qqHval = mmu.read_byte(self.registers.sp + 1)
        if qq == 'bc':
            self.registers.b = qqHval
            self.registers.c = qqLval
        elif qq == 'de':
            self.registers.d = qqHval
            self.registers.e = qqLval
        elif qq == 'hl':
            self.registers.h = qqHval
            self.registers.l = qqLval
        elif qq == 'af':
            self.registers.a = qqHval
            self.registers.f = qqLval
        self.registers.sp += 2
        self.registers.m = 3

    #region POP Shortcuts
    def POP_bc(self):
        self.POP_qq('bc')
    def POP_de(self):
        self.POP_qq('de')
    def POP_hl(self):
        self.POP_qq('hl')
    def POP_af(self):
        self.POP_qq('af')
    #endregion

    def LDHLsp_e(self):
        self.clear_flags()
        value = mmu.read_byte(self.registers.pc)
        if value > 127:
            value = - ((~value+1)&0xFF)
        self.registers.pc += 1
        value += self.registers.sp
        if value > 0xFFFF:
            self.flags.cy = True
        self.registers.h = (value >> 8) & 0xFF
        self.registers.l = value & 0xFF
        self.registers.m = 3

    def LDnn_sp(self):
        l_adrs = mmu.read_byte(self.registers.pc)
        h_adrs = mmu.read_byte(self.registers.pc + 1)
        self.registers.pc += 2
        addr = (h_adrs << 8) + l_adrs
        mmu.write_byte(addr,self.registers.sp & 0xFF)
        mmu.write_byte(addr + 1,self.registers.sp >> 8)
        self.registers.m = 5

    #endregion

    #region 8-Bit Arithmetic and Logical Operation Instructions

    #region Addition
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

    #region ADDr Shortcuts
    def ADDa(self):
        self.ADDr('a')
    def ADDb(self):
        self.ADDr('b')
    def ADDc(self):
        self.ADDr('c')
    def ADDd(self):
        self.ADDr('d')
    def ADDe(self):
        self.ADDr('e')
    def ADDh(self):
        self.ADDr('h')
    def ADDl(self):
        self.ADDr('l')
    #endregion

    def ADDn(self):
        self.clear_flags()
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
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

    def ADDa_hl(self):
        self.clear_flags()
        hlval = self.get_hl_value()
        #check for half-carry
        if (hlval & 0xF) + (self.registers.a & 0xF) > 15:
            self.flags.h = True
            #add immediate operand n to register a
        self.registers.a += hlval
        #check for carry
        if self.registers.a > 255:
            self.flags.cy = True
            #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    def ADCa_r(self,r):
        #need to have the name of the register here NOT the bitcode
        carry = self.flags.cy
        self.clear_flags()
        value = getattr(self.registers, r)

        #check for half-carry
        if (value & 0xF) + (self.registers.a & 0xf) > 15:
            self.flags.h = True
            #add register r to register a
        self.registers.a += value
        if carry:
            self.registers.a += 1
        #add carry
        #check for carry
        if self.registers.a > 255:
            self.flags.cy = True
            #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 1

    #region ADca Shortcuts
    def ADCa_a(self):
        self.ADCa_r('a')
    def ADCa_b(self):
        self.ADCa_r('b')
    def ADCa_c(self):
        self.ADCa_r('c')
    def ADCa_d(self):
        self.ADCa_r('d')
    def ADCa_e(self):
        self.ADCa_r('e')
    def ADCa_h(self):
        self.ADCa_r('h')
    def ADCa_l(self):
        self.ADCa_r('l')
    #endregion

    def ADCa_n(self):
        carry = self.flags.cy
        self.clear_flags()
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        if carry:
            n += 1
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

    def ADCa_hl(self):
        carry = self.flags.cy
        self.clear_flags()

        hlval = self.get_hl_value()
        if carry:
            hlval += 1
        #check for half-carry
        if (hlval & 0xF) + (self.registers.a & 0xF) > 15:
            self.flags.h = True
            #add immediate operand n to register a
        self.registers.a += hlval
        #check for carry
        if self.registers.a > 255:
            self.flags.cy = True
            #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    #endregion Addition

    #region Subtraction

    def SUBr(self,r):
        #need to have the name of the register here NOT the bitcode
        self.clear_flags()
        #check for half-carry
        if ((self.registers.a & 0xf) - getattr(self.registers, r) & 0xF) >= 15:
            self.flags.h = True
        #subtract register r from register a
        self.registers.a -= getattr(self.registers, r)
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 1

    #region SUB Shortcuts
    def SUBa(self):
        self.SUBr('a')
    def SUBb(self):
        self.SUBr('b')
    def SUBc(self):
        self.SUBr('c')
    def SUBd(self):
        self.SUBr('d')
    def SUBe(self):
        self.SUBr('e')
    def SUBh(self):
        self.SUBr('h')
    def SUBl(self):
        self.SUBr('l')
    #endregion

    def SUBn(self):
        #need to have the name of the register here NOT the bitcode
        self.clear_flags()
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        #check for half-carry
        if ((self.registers.a & 0xf) - n & 0xF) >= 15:
            self.flags.h = True
        #subtract immediate operand n from register a
        self.registers.a -= n
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 2

    def SUBhl(self):
        self.clear_flags()
        hlval = self.get_hl_value()
        #check for half-carry
        if ((self.registers.a & 0xf) - hlval & 0xF) >= 15:
            self.flags.h = True
        self.registers.a -= hlval
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 2

    def SBCa_r(self,r):
        #need to have the name of the register here NOT the bitcode
        carry = self.flags.cy
        self.clear_flags()
        #check for half-carry
        if ((self.registers.a & 0xf) - getattr(self.registers, r) & 0xF) >= 15:
            self.flags.h = True
        #subtract register r from register a
        self.registers.a -= getattr(self.registers, r)
        if carry:
            self.registers.a -= 1
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 1

    def SBCa_a(self):
        self.SBCa_r('a')
    def SBCa_b(self):
        self.SBCa_r('b')
    def SBCa_c(self):
        self.SBCa_r('c')
    def SBCa_d(self):
        self.SBCa_r('d')
    def SBCa_e(self):
        self.SBCa_r('e')
    def SBCa_h(self):
        self.SBCa_r('h')
    def SBCa_l(self):
        self.SBCa_r('l')

    def SBCa_n(self):
        a = self.registers.a
        carry = self.flags.cy
        self.clear_flags()
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        #check for half-carry
        if ((self.registers.a & 0xf) - n & 0xF) >= 15:
            self.flags.h = True
        #subtract immediate operand n from register a
        self.registers.a -= n
        if carry:
            self.registers.a -= 1
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 2

    def SBCa_hl(self):
        a = self.registers.a
        carry = self.flags.cy
        self.clear_flags()
        hlval = self.get_hl_value()
        if carry:
            hlval += 1
        #check for half-carry
        if (self.registers.a ^ hlval ^ a)&0x10 > 15:
            self.flags.h = True
        self.registers.a -= hlval
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
        #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 2

    def ANDr(self,r):
        self.clear_flags()
        self.registers.a = self.registers.a & getattr(self.registers,r)
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.h = True
        self.registers.m = 1

    #region ANDr Shortcuts
    def ANDa(self):
        self.ANDr('a')
    def ANDb(self):
        self.ANDr('b')
    def ANDc(self):
        self.ANDr('c')
    def ANDd(self):
        self.ANDr('d')
    def ANDe(self):
        self.ANDr('e')
    def ANDh(self):
        self.ANDr('h')
    def ANDl(self):
        self.ANDr('l')

    #endregion

    def ANDn(self):
        self.clear_flags()
        n = mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        self.registers.a = self.registers.a & n
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.h = True
        self.registers.m += 2

    def ANDhl(self):
        self.clear_flags()
        hlval = self.get_hl_value()
        self.registers.a = self.registers.a & hlval
        if self.registers.a == 0:
            self.flags.z = True
        temp = ((self.registers.a&0xf) + (hlval&0xf))&0x10
        self.flags.h = True
        self.registers.m += 2


    def NOP(self):
        self.registers.m = 1


class MMU(object):
    def __init__(self):
        self.in_bios = True
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
        self.rom = [0 for i in range(32768)]
        self.wram = [0 for i in range(8192)]
        self.eram = [0 for i in range(8192)]
        self.zram = [0 for i in range(8192)] # guessing the size here, probably wrong


    def read_byte(self, addr):
        if addr < 0x1000:
            if self.in_bios:
                if addr < 0x0100:
                    return self.bios[addr]
                elif cpu.registers.pc == 0x0100:
                    self.in_bios = False
                    #return nothing here ?
            return self.rom[addr]
        #Rom 0
        elif 0x1000 >= addr < 0x4000:
            return self.rom[addr]
        #Rom 1
        elif 0x4000 >= addr < 0x8000:
            return self.rom[addr]
        #VRAM
        elif 0x8000 >= addr < 0xA000:
            return gpu.vram[addr & 0x1FFF]

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
                    return gpu.oam[addr & 0xFF]
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
            if self.in_bios:
                if addr < 0x0100:
                    self.bios[addr] = value
                else:
                    self.rom[addr] = value
            else:
                self.rom[addr] = value
        #Rom 0
        elif 0x1000 >= addr < 0x4000:
            self.rom[addr] = value
        #Rom 1
        elif 0x4000 >= addr < 0x8000:
            self.rom[addr] = value
        #VRAM
        elif 0x8000 >= addr < 0xA000:
            gpu.vram[addr & 0x1FFF] = value

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
                    gpu.oam[addr & 0xFF] = value
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
        self.vram = [0 for i in range(16384)] #16kb vram
        self.oam = []


cpu = CPU()
gpu = GPU()
mmu = MMU()

