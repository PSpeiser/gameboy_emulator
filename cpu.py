class CPU(object):
    def __init__(self, mmu=None):
        self.mmu = mmu
        self.halt = False
        self.stop = False

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
    def get_register_pair(self, register_pair):
        if register_pair == 'bc':
            return (self.registers.b << 8) + self.registers.c
        elif register_pair == 'de':
            return (self.registers.d << 8) + self.registers.e
        elif register_pair == 'hl':
            return (self.registers.h << 8) + self.registers.l
        elif register_pair == 'sp':
            return self.registers.sp

    def set_register_pair(self, register_pair, value):
        if register_pair == 'bc':
            self.registers.b = (value >> 8) & 0xFF
            self.registers.c = value & 0xFF
        elif register_pair == 'de':
            self.registers.d = (value >> 8) & 0xFF
            self.registers.e = value & 0xFF
        elif register_pair == 'hl':
            self.registers.h = (value >> 8) & 0xFF
            self.registers.l = value & 0xFF
        elif register_pair == 'sp':
            self.registers.sp = value & 0xFFFF


    def get_immediate_operand(self):
        value = self.mmu.read_byte(self.registers.pc)
        self.registers.pc += 1
        return value

    def clear_flags(self):
        self.flags.z = False
        self.flags.n = False
        self.flags.h = False
        self.flags.cy = False


    #endregion

    #region 8-Bit Transfer and Input/Output Instructions
    def LDr_r(self, r, r2):
        setattr(self.registers, r, getattr(self.registers, r2))
        self.registers.m = 1

    #region LDr_r Shortcuts

    def LDa_a(self):
        self.LDr_r('a', 'a')

    def LDa_b(self):
        self.LDr_r('a', 'b')

    def LDa_c(self):
        self.LDr_r('a', 'c')

    def LDa_d(self):
        self.LDr_r('a', 'd')

    def LDa_e(self):
        self.LDr_r('a', 'e')

    def LDa_h(self):
        self.LDr_r('a', 'h')

    def LDa_l(self):
        self.LDr_r('a', 'l')

    def LDb_a(self):
        self.LDr_r('b', 'a')

    def LDb_b(self):
        self.LDr_r('b', 'b')

    def LDb_c(self):
        self.LDr_r('b', 'c')

    def LDb_d(self):
        self.LDr_r('b', 'd')

    def LDb_e(self):
        self.LDr_r('b', 'e')

    def LDb_h(self):
        self.LDr_r('b', 'h')

    def LDb_l(self):
        self.LDr_r('b', 'l')

    def LDc_a(self):
        self.LDr_r('c', 'a')

    def LDc_b(self):
        self.LDr_r('c', 'b')

    def LDc_c(self):
        self.LDr_r('c', 'c')

    def LDc_d(self):
        self.LDr_r('c', 'd')

    def LDc_e(self):
        self.LDr_r('c', 'e')

    def LDc_h(self):
        self.LDr_r('c', 'h')

    def LDc_l(self):
        self.LDr_r('c', 'l')

    def LDd_a(self):
        self.LDr_r('d', 'a')

    def LDd_b(self):
        self.LDr_r('d', 'b')

    def LDd_c(self):
        self.LDr_r('d', 'c')

    def LDd_d(self):
        self.LDr_r('d', 'd')

    def LDd_e(self):
        self.LDr_r('d', 'e')

    def LDd_h(self):
        self.LDr_r('d', 'h')

    def LDd_l(self):
        self.LDr_r('d', 'l')

    def LDe_a(self):
        self.LDr_r('e', 'a')

    def LDe_b(self):
        self.LDr_r('e', 'b')

    def LDe_c(self):
        self.LDr_r('e', 'c')

    def LDe_d(self):
        self.LDr_r('e', 'd')

    def LDe_e(self):
        self.LDr_r('e', 'e')

    def LDe_h(self):
        self.LDr_r('e', 'h')

    def LDe_l(self):
        self.LDr_r('e', 'l')

    def LDh_a(self):
        self.LDr_r('h', 'a')

    def LDh_b(self):
        self.LDr_r('h', 'b')

    def LDh_c(self):
        self.LDr_r('h', 'c')

    def LDh_d(self):
        self.LDr_r('h', 'd')

    def LDh_e(self):
        self.LDr_r('h', 'e')

    def LDh_h(self):
        self.LDr_r('h', 'h')

    def LDh_l(self):
        self.LDr_r('h', 'l')

    def LDl_a(self):
        self.LDr_r('l', 'a')

    def LDl_b(self):
        self.LDr_r('l', 'b')

    def LDl_c(self):
        self.LDr_r('l', 'c')

    def LDl_d(self):
        self.LDr_r('l', 'd')

    def LDl_e(self):
        self.LDr_r('l', 'e')

    def LDl_h(self):
        self.LDr_r('l', 'h')

    def LDl_l(self):
        self.LDr_r('l', 'l')

        #endregion

    def LDr_n(self, r):
        n = self.get_immediate_operand()
        setattr(self.registers, r, n)
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

    def LDr_hl(self, r):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        setattr(self.registers, r, value)
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


    def LDhl_r(self, r):
        addr = self.get_register_pair('hl')
        value = getattr(self.registers, r)
        self.mmu.write_byte(addr, value)
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
        n = self.get_immediate_operand()
        addr = self.get_register_pair('hl')
        self.mmu.write_byte(addr, n)
        self.registers.m = 3

    def LDa_bc(self):
        value = self.mmu.read_byte(self.get_register_pair('bc'))
        self.registers.a = value
        self.registers.m = 2

    def LDa_de(self):
        value = self.mmu.read_byte(self.get_register_pair('de'))
        self.registers.a = value
        self.registers.m = 2

    def LDa_c(self):
        addr = 0xFF00 + self.registers.c
        value = self.mmu.read_byte(addr)
        self.registers.a = value
        self.registers.m = 2

    def LDc_a(self):
        addr = 0xFF00 + self.registers.c
        self.mmu.write_byte(addr, self.registers.a)
        self.registers.m = 2

    def LDa_n(self):
        n = self.get_immediate_operand()
        self.registers.a = self.mmu.read_byte(0xFF00 + n)
        self.registers.m = 3

    def LDn_a(self):
        n = self.get_immediate_operand()
        self.mmu.write_byte(n, self.registers.a)
        self.registers.m = 3

    def LDa_nn(self):
        n = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.registers.a = self.mmu.read_byte(n)
        self.registers.m = 4

    def LDnn_a(self):
        n = self.mmu.read_word(self.registers.pc)
        self.registers.pc += 2
        self.mmu.write_byte(n, self.registers.a)
        self.registers.m = 4

    def LDa_hli(self):
        addr = self.get_register_pair('hl')
        self.registers.a = self.mmu.read_byte(addr)
        #increment hl
        addr += 1
        self.registers.h = (addr >> 8) & 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDa_hld(self):
        addr = self.get_register_pair('hl')
        self.registers.a = self.mmu.read_byte(addr)
        #decrement hl
        addr -= 1
        self.registers.h = (addr >> 8) & 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDbc_a(self):
        addr = self.get_register_pair('bc')
        self.mmu.write_byte(addr, self.registers.a)
        self.registers.m = 2

    def LDde_a(self):
        addr = self.get_register_pair('de')
        self.mmu.write_byte(addr, self.registers.a)
        self.registers.m = 2

    def LDhli_a(self):
        addr = self.get_register_pair('hl')
        self.mmu.write_byte(addr, self.registers.a)
        #increment hl
        addr += 1
        self.registers.h = (addr >> 8) & 0xFF
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    def LDhld_a(self):
        addr = self.get_register_pair('hl')
        self.mmu.write_byte(addr, self.registers.a)
        #decrement hl
        addr -= 1
        self.registers.h = addr >> 8
        self.registers.l = addr & 0xFF
        self.registers.m = 2

    #endregion

    #region 16-Bit Transfer Instructions
    def LDdd_nn(self, dd):
        nn = self.mmu.read_word(self.registers.pc)
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
        self.registers.sp = self.get_register_pair('hl')
        self.registers.m = 2

    def PUSH_qq(self, qq):
        if qq == 'bc':
            qqH = self.registers.b
            qqL = self.registers.c
        elif qq == 'de':
            qqH = self.registers.d
            qqL = self.registers.e
        elif qq == 'hl':
            qqH = self.registers.h
            qqL = self.registers.l
        elif qq == 'af':
            qqH = self.registers.a
            qqL = self.registers.f
        self.mmu.write_byte(self.registers.sp - 1, qqH)
        self.mmu.write_byte(self.registers.sp - 2, qqL)
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

    def POP_qq(self, qq):
        qqLval = self.mmu.read_byte(self.registers.sp)
        qqHval = self.mmu.read_byte(self.registers.sp + 1)
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
        value = self.get_immediate_operand()
        if value > 127:
            value = - ((~value + 1) & 0xFF)
        value += self.registers.sp
        if value > 0xFFFF:
            self.flags.cy = True
        self.set_register_pair('hl', value)
        self.registers.m = 3

    def LDnn_sp(self):
        l_adrs = self.get_immediate_operand()
        h_adrs = self.get_immediate_operand()
        self.registers.pc += 2
        addr = (h_adrs << 8) + l_adrs
        self.mmu.write_byte(addr, self.registers.sp & 0xFF)
        self.mmu.write_byte(addr + 1, self.registers.sp >> 8)
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
        n = self.get_immediate_operand()
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
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
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

    def ADCa_r(self, r):
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
        n = self.get_immediate_operand()
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

        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
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

    def SUBr(self, r):
        #var a=Z80._r.a;
        # Z80._r.a-=Z80._r.b;
        # Z80._r.f=(Z80._r.a<0)?0x50:0x40;
        # Z80._r.a&=255;
        # if(!Z80._r.a)
        # Z80._r.f|=0x80;
        # if((Z80._r.a^Z80._r.b^a)&0x10)
        # Z80._r.f|=0x20;
        # Z80._r.m=1;
        #need to have the name of the register here NOT the bitcode
        a = self.registers.a
        self.registers.a -= getattr(self.registers, r)
        self.clear_flags()
        self.flags.cy = self.registers.a < 0
        self.flags.n = True
        #mask to 8 bits
        self.registers.a &= 255
        #check for zero
        if self.registers.a == 0:
            self.flags.z = True
            #check for half-carry
        if (self.registers.a ^ self.registers.b ^ a) & 0x10:
            self.flags.h = True

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
        a = self.registers.a
        n = self.get_immediate_operand()
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
            #check for half-carry
        if (self.registers.a ^ n ^ a) & 0x10:
            self.flags.h = True
        self.flags.n = True
        self.registers.m = 2

    def SUBhl(self):
        self.clear_flags()
        a = self.registers.a
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        self.registers.a -= hlval
        #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
            #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for half-carry
        if (self.registers.a ^ hlval ^ a) & 0x10:
            self.flags.h = True
            #check for zero
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.n = True
        self.registers.m = 2

    def SBCa_r(self, r):
        #need to have the name of the register here NOT the bitcode
        carry = self.flags.cy
        self.clear_flags()
        a = self.registers.a
        #subtract register r from register a
        n = getattr(self.registers, r)
        self.registers.a -= n
        if carry:
            self.registers.a -= 1
            #check for carry
        if self.registers.a < 0:
            self.flags.cy = True
            #mask to 8 bits
        self.registers.a = self.registers.a & 255
        #check for half-carry
        if (self.registers.a ^ n ^ a) & 0x10:
            self.flags.h = True
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
        n = self.get_immediate_operand()
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
            #check for half-carry
        if (self.registers.a ^ n ^ a) & 0x10:
            self.flags.h = True
        self.flags.n = True
        self.registers.m = 2

    def SBCa_hl(self):
        a = self.registers.a
        carry = self.flags.cy
        self.clear_flags()
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        if carry:
            hlval += 1
            #check for half-carry
        if (self.registers.a ^ hlval ^ a) & 0x10 > 15:
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

    def ANDr(self, r):
        self.clear_flags()
        self.registers.a = self.registers.a & getattr(self.registers, r)
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
        n = self.get_immediate_operand()
        self.registers.a = self.registers.a & n
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.h = True
        self.registers.m = 2

    def ANDhl(self):
        self.clear_flags()
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        self.registers.a = self.registers.a & hlval
        if self.registers.a == 0:
            self.flags.z = True
        self.flags.h = True
        self.registers.m = 2

    def ORr(self, r):
        self.clear_flags()
        self.registers.a = self.registers.a | getattr(self.registers, r)
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 1

    #region ORr Shortcuts
    def ORa(self):
        self.ORr('a')

    def ORb(self):
        self.ORr('b')

    def ORc(self):
        self.ORr('c')

    def ORd(self):
        self.ORr('d')

    def ORe(self):
        self.ORr('e')

    def ORh(self):
        self.ORr('h')

    def ORl(self):
        self.ORr('l')

        #endregion

    def ORn(self):
        self.clear_flags()
        n = self.get_immediate_operand()
        self.registers.a = self.registers.a | n
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    def ORhl(self):
        self.clear_flags()
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        self.registers.a = self.registers.a | hlval
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    def XORr(self, r):
        self.clear_flags()
        self.registers.a = self.registers.a ^ getattr(self.registers, r)
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 1

    #region ORr Shortcuts
    def XORa(self):
        self.XORr('a')

    def XORb(self):
        self.XORr('b')

    def XORc(self):
        self.XORr('c')

    def XORd(self):
        self.XORr('d')

    def XORe(self):
        self.XORr('e')

    def XORh(self):
        self.XORr('h')

    def XORl(self):
        self.XORr('l')

    #endregion

    def XORn(self):
        self.clear_flags()
        n = self.get_immediate_operand()
        self.registers.a = self.registers.a ^ n
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    def XORhl(self):
        self.clear_flags()
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        self.registers.a = self.registers.a ^ hlval
        if self.registers.a == 0:
            self.flags.z = True
        self.registers.m = 2

    def CPr(self, r):
        self.clear_flags()
        value = getattr(self.registers, r)
        result = self.registers.a - value
        if result == 0:
            self.flags.z = True
            #check for carry
        if result < 0:
            self.flags.cy = True
        temp = (result ^ value ^ self.registers.a) & 0x10
        t2 = ((self.registers.a & 0xF) - (value & 0xf)) & 0x10
        if (result ^ value ^ self.registers.a) & 0x10 > 15:
            self.flags.h = True
        self.flags.n = True
        self.registers.m = 1

    #region CPr Shortcuts

    def CPa(self):
        self.CPr('a')

    def CPb(self):
        self.CPr('b')

    def CPc(self):
        self.CPr('c')

    def CPd(self):
        self.CPr('d')

    def CPe(self):
        self.CPr('e')

    def CPh(self):
        self.CPr('h')

    def CPl(self):
        self.CPr('l')

    #endregion

    def CPn(self):
        self.clear_flags()
        value = self.get_immediate_operand()
        result = self.registers.a - value
        if result == 0:
            self.flags.z = True
            #check for carry
        if result < 0:
            self.flags.cy = True
        temp = (result ^ value ^ self.registers.a) & 0x10
        t2 = ((self.registers.a & 0xF) - (value & 0xf)) & 0x10
        if (result ^ value ^ self.registers.a) & 0x10 > 15:
            self.flags.h = True
        self.flags.n = True
        self.registers.m = 2

    def CPhl(self):
        self.clear_flags()
        value = self.mmu.read_byte(self.get_register_pair('hl'))
        result = self.registers.a - value
        if result == 0:
            self.flags.z = True
            #check for carry
        if result < 0:
            self.flags.cy = True
        if (result ^ value ^ self.registers.a) & 0x10 > 15:
            self.flags.h = True
        self.flags.n = True
        self.registers.m = 2

    def INCr(self, r):
        self.clear_flags()
        #increment register by one
        value = getattr(self.registers, r) + 1
        #check for overflow
        if value > 255:
            self.flags.cy = True
            #check for half-carry
        if (1 & 0xF) + (self.registers.a & 0xF) > 15:
            self.flags.h = True
            #mask the register to 8 bits
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 1

    #region INCr Shortcuts
    def INCa(self):
        self.INCr('a')

    def INCb(self):
        self.INCr('b')

    def INCc(self):
        self.INCr('c')

    def INCd(self):
        self.INCr('d')

    def INCe(self):
        self.INCr('e')

    def INCh(self):
        self.INCr('h')

    def INCl(self):
        self.INCr('l')

        #endregion

    def INChl(self):
        self.clear_flags()
        hlvalue = self.mmu.read_byte(self.get_register_pair('hl')) + 1
        if (1 & 0xF) + (hlvalue & 0xF) > 15:
            self.flags.h = True
        if hlvalue > 255:
            self.flags.cy = True
        hlvalue = hlvalue & 0xFF
        if hlvalue == 0:
            self.flags.z = True
        self.mmu.write_byte(self.get_register_pair('hl'), hlvalue)

    def DECr(self, r):
        self.clear_flags()
        #DECrement register by one
        value = getattr(self.registers, r) - 1
        #check for underflow
        if value < 0:
            self.flags.cy = True
            #check for half-carry
        if (1 & 0xF) + (self.registers.a & 0xF) > 15:
            self.flags.h = True
            #mask the register to 8 bits
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.flags.n = True
        setattr(self.registers, r, value)
        self.registers.m = 1

    #region DECr Shortcuts
    def DECa(self):
        self.DECr('a')

    def DECb(self):
        self.DECr('b')

    def DECc(self):
        self.DECr('c')

    def DECd(self):
        self.DECr('d')

    def DECe(self):
        self.DECr('e')

    def DECh(self):
        self.DECr('h')

    def DECl(self):
        self.DECr('l')

        #endregion

    def DEChl(self):
        self.clear_flags()
        hlvalue = self.mmu.read_byte(self.get_register_pair('hl')) - 1
        if (1 & 0xF) + (hlvalue & 0xF) > 15:
            self.flags.h = True
        if hlvalue < 0:
            self.flags.cy = True
        hlvalue = hlvalue & 0xFF
        if hlvalue == 0:
            self.flags.z = True
        self.flags.n = True
        self.mmu.write_byte(self.get_register_pair('hl'), hlvalue)
        self.registers.m = 3

    def ADDhl_ss(self, ss):
        self.clear_flags()
        hlvalue = self.get_register_pair('hl')
        ssvalue = self.get_register_pair(ss)
        value = hlvalue + ssvalue
        if (ssvalue & 0xFF) + (hlvalue & 0xFF) > 0xF:
            self.flags.h = True
        if value > 0xFFFF:
            self.flags.cy = True
        value = value & 0xFFFF
        self.set_register_pair('hl', value)
        self.registers.m = 2

    def ADDhl_bc(self):
        self.ADDhl_ss('bc')

    def ADDhl_de(self):
        self.ADDhl_ss('de')

    def ADDhl_hl(self):
        self.ADDhl_ss('hl')

    def ADDhl_sp(self):
        self.ADDhl_ss('sp')

    def ADDsp_e(self):
        self.clear_flags()
        e = self.get_immediate_operand()
        value = self.registers.sp + e
        if (self.registers.sp & 0xFF) + (e & 0xFF) > 0xFF:
            self.flags.h = True
        if value > 0xFFFF:
            self.flags.cy = True
        value = value & 0xFFFF
        if value == 0:
            self.flags.z = True
        self.registers.sp = value
        self.registers.m = 4

    def INC_ss(self, ss):
        self.clear_flags()
        self.set_register_pair(ss, self.get_register_pair(ss) + 1)
        self.registers.m = 2

    def INC_ss_bc(self):
        self.INC_ss('bc')

    def INC_ss_de(self):
        self.INC_ss('de')

    def INC_ss_hl(self):
        self.INC_ss('hl')

    def INC_ss_sp(self):
        self.INC_ss('sp')

    def DEC_ss(self, ss):
        self.clear_flags()
        self.set_register_pair(ss, self.get_register_pair(ss) - 1)
        self.registers.m = 2

    def DEC_ss_bc(self):
        self.DEC_ss('bc')

    def DEC_ss_de(self):
        self.DEC_ss('de')

    def DEC_ss_hl(self):
        self.DEC_ss('hl')

    def DEC_ss_sp(self):
        self.DEC_ss('sp')

    def RLCA(self):
        value = self.registers.a << 1
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value > 0xFF
        if carry:
            #bit 0 should be set to 1 here according to the documentation, example test fails in that case
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.registers.a = value
        self.registers.m = 1

    def RLA(self):
        value = self.registers.a << 1
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.registers.a = value
        self.registers.m = 1

    def RRCA(self):
        value = self.registers.a
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
            value = value | 0x80
        if value == 0:
            self.flags.z = True
        self.registers.a = value
        self.registers.m = 1

    def RRA(self):
        value = self.registers.a
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
        if value == 0:
            self.flags.z = True
        self.registers.a = value
        self.registers.m = 1

    def RLC_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
            if value % 2 == 0:
                value += 1
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 2

    def RLC_a(self):
        self.RLC_r('%s')

    def RLC_b(self):
        self.RLC_r('%s')

    def RLC_c(self):
        self.RLC_r('%s')

    def RLC_d(self):
        self.RLC_r('%s')

    def RLC_e(self):
        self.RLC_r('%s')

    def RLC_h(self):
        self.RLC_r('%s')

    def RLC_l(self):
        self.RLC_r('%s')

    def RLC_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
            if value % 2 == 0:
                value += 1
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def RL_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 2

    def Rl_a(self):
        self.RL_r('a')

    def Rl_b(self):
        self.RL_r('b')

    def Rl_c(self):
        self.RL_r('c')

    def Rl_d(self):
        self.RL_r('d')

    def Rl_e(self):
        self.RL_r('e')

    def Rl_h(self):
        self.RL_r('h')

    def Rl_l(self):
        self.RL_r('l')

    def RL_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def RRC_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
            value = value | 0x80
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 2

    def RRC_a(self):
        self.RRC_r('a')

    def RRC_b(self):
        self.RRC_r('b')

    def RRC_c(self):
        self.RRC_r('c')

    def RRC_d(self):
        self.RRC_r('d')

    def RRC_e(self):
        self.RRC_r('e')

    def RRC_h(self):
        self.RRC_r('h')

    def RRC_l(self):
        self.RRC_r('l')

    def RRC_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
            value = value | 0x80
        if value == 0:
            self.flags.z = True
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def RR_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 2

    def RR_a(self):
        self.RR_r('a')

    def RR_b(self):
        self.RR_r('b')

    def RR_c(self):
        self.RR_r('c')

    def RR_d(self):
        self.RR_r('d')

    def RR_e(self):
        self.RR_r('e')

    def RR_h(self):
        self.RR_r('h')

    def RR_l(self):
        self.RR_r('l')

    def RR_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        carry = value % 2 == 1
        value = value >> 1
        if carry:
            self.flags.cy = True
        if value == 0:
            self.flags.z = True
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def SLA_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()

        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        setattr(self.registers, r, value)
        self.registers.m = 2

    #region SLA_r Shortcuts

    def SLA_a(self):
        self.SLA_r('a')

    def SLA_b(self):
        self.SLA_r('b')

    def SLA_c(self):
        self.SLA_r('c')

    def SLA_d(self):
        self.SLA_r('d')

    def SLA_e(self):
        self.SLA_r('e')

    def SLA_h(self):
        self.SLA_r('h')

    def SLA_l(self):
        self.SLA_r('l')

    #endregion

    def SLA_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()

        value = value << 1
        carry = value > 0xFF
        if carry:
            self.flags.cy = True
        value = value & 0xFF
        if value == 0:
            self.flags.z = True
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def SRA_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        self.flags.cy = value % 2 == 1
        bit7set = value >= 0x80
        value = (value >> 1)
        if bit7set:
            value = value | 0x80
        self.flags.z = value == 0
        setattr(self.registers, r, value)
        self.registers.m = 2

    #region SRA Shortcuts
    def SRA_a(self):
        self.SRA_r('a')

    def SRA_b(self):
        self.SRA_r('b')

    def SRA_c(self):
        self.SRA_r('c')

    def SRA_d(self):
        self.SRA_r('d')

    def SRA_e(self):
        self.SRA_r('e')

    def SRA_h(self):
        self.SRA_r('h')

    def SRA_l(self):
        self.SRA_r('l')

        #endregion

    def SRA_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        self.flags.cy = value % 2 == 1
        bit7set = value >= 0x80
        value = (value >> 1)
        if bit7set:
            value = value | 0x80
        self.flags.z = value == 0
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def SRL_r(self, r):
        value = getattr(self.registers, r)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        self.flags.cy = value % 2 == 1
        value = (value >> 1)
        self.flags.z = value == 0
        setattr(self.registers, r, value)
        self.registers.m = 2

    def SRL_a(self):
        self.SRL_r('a')

    def SRL_b(self):
        self.SRL_r('b')

    def SRL_c(self):
        self.SRL_r('c')

    def SRL_d(self):
        self.SRL_r('d')

    def SRL_e(self):
        self.SRL_r('e')

    def SRL_h(self):
        self.SRL_r('h')

    def SRL_l(self):
        self.SRL_r('l')

    def SRL_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        if self.flags.cy:
            value += 1
        self.clear_flags()
        self.flags.cy = value % 2 == 1
        value = (value >> 1)
        self.flags.z = value == 0
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def SWAP_r(self, r):
        value = getattr(self.registers, r)
        self.clear_flags()
        hvalue = (value & 0x0F) << 4
        lvalue = (value & 0xF0) >> 4
        value = hvalue + lvalue
        self.flags.z = value == 0
        setattr(self.registers, r, value)
        self.registers.m = 2

    def SWAP_hl(self):
        addr = self.get_register_pair('hl')
        value = self.mmu.read_byte(addr)
        self.clear_flags()
        hvalue = (value & 0x0F) << 4
        lvalue = (value & 0xF0) >> 4
        value = hvalue + lvalue
        self.flags.z = value == 0
        self.mmu.write_byte(addr, value)
        self.registers.m = 4

    def BIT_b_r(self, b, r):
        #b is the int specifying the bit, r is a string specifying the register
        self.clear_flags()
        self.flags.z = (getattr(self.registers, r) >> b) % 2 == 0
        self.flags.h = True
        self.registers.m = 2

    #region BIT Shortcuts
    def BIT_0_a(self):
        self.BIT_b_r(0, 'a')

    def BIT_0_b(self):
        self.BIT_b_r(0, 'b')

    def BIT_0_c(self):
        self.BIT_b_r(0, 'c')

    def BIT_0_d(self):
        self.BIT_b_r(0, 'd')

    def BIT_0_e(self):
        self.BIT_b_r(0, 'e')

    def BIT_0_h(self):
        self.BIT_b_r(0, 'h')

    def BIT_0_l(self):
        self.BIT_b_r(0, 'l')

    def BIT_1_a(self):
        self.BIT_b_r(1, 'a')

    def BIT_1_b(self):
        self.BIT_b_r(1, 'b')

    def BIT_1_c(self):
        self.BIT_b_r(1, 'c')

    def BIT_1_d(self):
        self.BIT_b_r(1, 'd')

    def BIT_1_e(self):
        self.BIT_b_r(1, 'e')

    def BIT_1_h(self):
        self.BIT_b_r(1, 'h')

    def BIT_1_l(self):
        self.BIT_b_r(1, 'l')

    def BIT_2_a(self):
        self.BIT_b_r(2, 'a')

    def BIT_2_b(self):
        self.BIT_b_r(2, 'b')

    def BIT_2_c(self):
        self.BIT_b_r(2, 'c')

    def BIT_2_d(self):
        self.BIT_b_r(2, 'd')

    def BIT_2_e(self):
        self.BIT_b_r(2, 'e')

    def BIT_2_h(self):
        self.BIT_b_r(2, 'h')

    def BIT_2_l(self):
        self.BIT_b_r(2, 'l')

    def BIT_3_a(self):
        self.BIT_b_r(3, 'a')

    def BIT_3_b(self):
        self.BIT_b_r(3, 'b')

    def BIT_3_c(self):
        self.BIT_b_r(3, 'c')

    def BIT_3_d(self):
        self.BIT_b_r(3, 'd')

    def BIT_3_e(self):
        self.BIT_b_r(3, 'e')

    def BIT_3_h(self):
        self.BIT_b_r(3, 'h')

    def BIT_3_l(self):
        self.BIT_b_r(3, 'l')

    def BIT_4_a(self):
        self.BIT_b_r(4, 'a')

    def BIT_4_b(self):
        self.BIT_b_r(4, 'b')

    def BIT_4_c(self):
        self.BIT_b_r(4, 'c')

    def BIT_4_d(self):
        self.BIT_b_r(4, 'd')

    def BIT_4_e(self):
        self.BIT_b_r(4, 'e')

    def BIT_4_h(self):
        self.BIT_b_r(4, 'h')

    def BIT_4_l(self):
        self.BIT_b_r(4, 'l')

    def BIT_5_a(self):
        self.BIT_b_r(5, 'a')

    def BIT_5_b(self):
        self.BIT_b_r(5, 'b')

    def BIT_5_c(self):
        self.BIT_b_r(5, 'c')

    def BIT_5_d(self):
        self.BIT_b_r(5, 'd')

    def BIT_5_e(self):
        self.BIT_b_r(5, 'e')

    def BIT_5_h(self):
        self.BIT_b_r(5, 'h')

    def BIT_5_l(self):
        self.BIT_b_r(5, 'l')

    def BIT_6_a(self):
        self.BIT_b_r(6, 'a')

    def BIT_6_b(self):
        self.BIT_b_r(6, 'b')

    def BIT_6_c(self):
        self.BIT_b_r(6, 'c')

    def BIT_6_d(self):
        self.BIT_b_r(6, 'd')

    def BIT_6_e(self):
        self.BIT_b_r(6, 'e')

    def BIT_6_h(self):
        self.BIT_b_r(6, 'h')

    def BIT_6_l(self):
        self.BIT_b_r(6, 'l')

    def BIT_7_a(self):
        self.BIT_b_r(7, 'a')

    def BIT_7_b(self):
        self.BIT_b_r(7, 'b')

    def BIT_7_c(self):
        self.BIT_b_r(7, 'c')

    def BIT_7_d(self):
        self.BIT_b_r(7, 'd')

    def BIT_7_e(self):
        self.BIT_b_r(7, 'e')

    def BIT_7_h(self):
        self.BIT_b_r(7, 'h')

    def BIT_7_l(self):
        self.BIT_b_r(7, 'l')

        #endregion

    def BIT_b_hl(self, b):
        self.clear_flags()
        hlval = self.mmu.read_byte(self.get_register_pair('hl'))
        self.flags.z = (hlval >> b) % 2 == 0
        self.flags.h = True
        self.registers.m = 3

    #region BIT_b_hl Shortcuts
    def BIT_0_hl(self):
        self.BIT_b_hl(0)

    def BIT_1_hl(self):
        self.BIT_b_hl(1)

    def BIT_2_hl(self):
        self.BIT_b_hl(2)

    def BIT_3_hl(self):
        self.BIT_b_hl(3)

    def BIT_4_hl(self):
        self.BIT_b_hl(4)

    def BIT_5_hl(self):
        self.BIT_b_hl(5)

    def BIT_6_hl(self):
        self.BIT_b_hl(6)

    def BIT_7_hl(self):
        self.BIT_b_hl(7)

        #endregion

    def SET_b_r(self, b, r):
        self.clear_flags()
        value = getattr(self.registers, r) | 2 ** b
        setattr(self.registers, r, value)
        self.registers.m = 2

    #region SET Shortcuts
    def SET_0_a(self):
        self.SET_b_r(0, 'a')

    def SET_0_b(self):
        self.SET_b_r(0, 'b')

    def SET_0_c(self):
        self.SET_b_r(0, 'c')

    def SET_0_d(self):
        self.SET_b_r(0, 'd')

    def SET_0_e(self):
        self.SET_b_r(0, 'e')

    def SET_0_h(self):
        self.SET_b_r(0, 'h')

    def SET_0_l(self):
        self.SET_b_r(0, 'l')

    def SET_1_a(self):
        self.SET_b_r(1, 'a')

    def SET_1_b(self):
        self.SET_b_r(1, 'b')

    def SET_1_c(self):
        self.SET_b_r(1, 'c')

    def SET_1_d(self):
        self.SET_b_r(1, 'd')

    def SET_1_e(self):
        self.SET_b_r(1, 'e')

    def SET_1_h(self):
        self.SET_b_r(1, 'h')

    def SET_1_l(self):
        self.SET_b_r(1, 'l')

    def SET_2_a(self):
        self.SET_b_r(2, 'a')

    def SET_2_b(self):
        self.SET_b_r(2, 'b')

    def SET_2_c(self):
        self.SET_b_r(2, 'c')

    def SET_2_d(self):
        self.SET_b_r(2, 'd')

    def SET_2_e(self):
        self.SET_b_r(2, 'e')

    def SET_2_h(self):
        self.SET_b_r(2, 'h')

    def SET_2_l(self):
        self.SET_b_r(2, 'l')

    def SET_3_a(self):
        self.SET_b_r(3, 'a')

    def SET_3_b(self):
        self.SET_b_r(3, 'b')

    def SET_3_c(self):
        self.SET_b_r(3, 'c')

    def SET_3_d(self):
        self.SET_b_r(3, 'd')

    def SET_3_e(self):
        self.SET_b_r(3, 'e')

    def SET_3_h(self):
        self.SET_b_r(3, 'h')

    def SET_3_l(self):
        self.SET_b_r(3, 'l')

    def SET_4_a(self):
        self.SET_b_r(4, 'a')

    def SET_4_b(self):
        self.SET_b_r(4, 'b')

    def SET_4_c(self):
        self.SET_b_r(4, 'c')

    def SET_4_d(self):
        self.SET_b_r(4, 'd')

    def SET_4_e(self):
        self.SET_b_r(4, 'e')

    def SET_4_h(self):
        self.SET_b_r(4, 'h')

    def SET_4_l(self):
        self.SET_b_r(4, 'l')

    def SET_5_a(self):
        self.SET_b_r(5, 'a')

    def SET_5_b(self):
        self.SET_b_r(5, 'b')

    def SET_5_c(self):
        self.SET_b_r(5, 'c')

    def SET_5_d(self):
        self.SET_b_r(5, 'd')

    def SET_5_e(self):
        self.SET_b_r(5, 'e')

    def SET_5_h(self):
        self.SET_b_r(5, 'h')

    def SET_5_l(self):
        self.SET_b_r(5, 'l')

    def SET_6_a(self):
        self.SET_b_r(6, 'a')

    def SET_6_b(self):
        self.SET_b_r(6, 'b')

    def SET_6_c(self):
        self.SET_b_r(6, 'c')

    def SET_6_d(self):
        self.SET_b_r(6, 'd')

    def SET_6_e(self):
        self.SET_b_r(6, 'e')

    def SET_6_h(self):
        self.SET_b_r(6, 'h')

    def SET_6_l(self):
        self.SET_b_r(6, 'l')

    def SET_7_a(self):
        self.SET_b_r(7, 'a')

    def SET_7_b(self):
        self.SET_b_r(7, 'b')

    def SET_7_c(self):
        self.SET_b_r(7, 'c')

    def SET_7_d(self):
        self.SET_b_r(7, 'd')

    def SET_7_e(self):
        self.SET_b_r(7, 'e')

    def SET_7_h(self):
        self.SET_b_r(7, 'h')

    def SET_7_l(self):
        self.SET_b_r(7, 'l')

        #endregion

    def SET_b_hl(self, b):
        self.clear_flags()
        addr = self.get_register_pair('hl')
        hlval = self.mmu.read_byte(addr)
        hlval = hlval | 2 ** b
        self.mmu.write_byte(addr, hlval)
        self.registers.m = 4

    #region SET_b_hl Shortcuts
    def SET_0_hl(self):
        self.SET_b_hl(0)

    def SET_1_hl(self):
        self.SET_b_hl(1)

    def SET_2_hl(self):
        self.SET_b_hl(2)

    def SET_3_hl(self):
        self.SET_b_hl(3)

    def SET_4_hl(self):
        self.SET_b_hl(4)

    def SET_5_hl(self):
        self.SET_b_hl(5)

    def SET_6_hl(self):
        self.SET_b_hl(6)

    def SET_7_hl(self):
        self.SET_b_hl(7)

        #endregion

    def RES_b_r(self, b, r):
        self.clear_flags()
        notval = ~(2 ** b)
        value = getattr(self.registers, r) & notval
        setattr(self.registers, r, value)
        self.registers.m = 2

    #region RES_b_r Shortcuts
    def RES_0_a(self):
        self.RES_b_r(0, 'a')

    def RES_0_b(self):
        self.RES_b_r(0, 'b')

    def RES_0_c(self):
        self.RES_b_r(0, 'c')

    def RES_0_d(self):
        self.RES_b_r(0, 'd')

    def RES_0_e(self):
        self.RES_b_r(0, 'e')

    def RES_0_h(self):
        self.RES_b_r(0, 'h')

    def RES_0_l(self):
        self.RES_b_r(0, 'l')

    def RES_1_a(self):
        self.RES_b_r(1, 'a')

    def RES_1_b(self):
        self.RES_b_r(1, 'b')

    def RES_1_c(self):
        self.RES_b_r(1, 'c')

    def RES_1_d(self):
        self.RES_b_r(1, 'd')

    def RES_1_e(self):
        self.RES_b_r(1, 'e')

    def RES_1_h(self):
        self.RES_b_r(1, 'h')

    def RES_1_l(self):
        self.RES_b_r(1, 'l')

    def RES_2_a(self):
        self.RES_b_r(2, 'a')

    def RES_2_b(self):
        self.RES_b_r(2, 'b')

    def RES_2_c(self):
        self.RES_b_r(2, 'c')

    def RES_2_d(self):
        self.RES_b_r(2, 'd')

    def RES_2_e(self):
        self.RES_b_r(2, 'e')

    def RES_2_h(self):
        self.RES_b_r(2, 'h')

    def RES_2_l(self):
        self.RES_b_r(2, 'l')

    def RES_3_a(self):
        self.RES_b_r(3, 'a')

    def RES_3_b(self):
        self.RES_b_r(3, 'b')

    def RES_3_c(self):
        self.RES_b_r(3, 'c')

    def RES_3_d(self):
        self.RES_b_r(3, 'd')

    def RES_3_e(self):
        self.RES_b_r(3, 'e')

    def RES_3_h(self):
        self.RES_b_r(3, 'h')

    def RES_3_l(self):
        self.RES_b_r(3, 'l')

    def RES_4_a(self):
        self.RES_b_r(4, 'a')

    def RES_4_b(self):
        self.RES_b_r(4, 'b')

    def RES_4_c(self):
        self.RES_b_r(4, 'c')

    def RES_4_d(self):
        self.RES_b_r(4, 'd')

    def RES_4_e(self):
        self.RES_b_r(4, 'e')

    def RES_4_h(self):
        self.RES_b_r(4, 'h')

    def RES_4_l(self):
        self.RES_b_r(4, 'l')

    def RES_5_a(self):
        self.RES_b_r(5, 'a')

    def RES_5_b(self):
        self.RES_b_r(5, 'b')

    def RES_5_c(self):
        self.RES_b_r(5, 'c')

    def RES_5_d(self):
        self.RES_b_r(5, 'd')

    def RES_5_e(self):
        self.RES_b_r(5, 'e')

    def RES_5_h(self):
        self.RES_b_r(5, 'h')

    def RES_5_l(self):
        self.RES_b_r(5, 'l')

    def RES_6_a(self):
        self.RES_b_r(6, 'a')

    def RES_6_b(self):
        self.RES_b_r(6, 'b')

    def RES_6_c(self):
        self.RES_b_r(6, 'c')

    def RES_6_d(self):
        self.RES_b_r(6, 'd')

    def RES_6_e(self):
        self.RES_b_r(6, 'e')

    def RES_6_h(self):
        self.RES_b_r(6, 'h')

    def RES_6_l(self):
        self.RES_b_r(6, 'l')

    def RES_7_a(self):
        self.RES_b_r(7, 'a')

    def RES_7_b(self):
        self.RES_b_r(7, 'b')

    def RES_7_c(self):
        self.RES_b_r(7, 'c')

    def RES_7_d(self):
        self.RES_b_r(7, 'd')

    def RES_7_e(self):
        self.RES_b_r(7, 'e')

    def RES_7_h(self):
        self.RES_b_r(7, 'h')

    def RES_7_l(self):
        self.RES_b_r(7, 'l')

        #endregion

    def RES_b_hl(self, b):
        self.clear_flags()
        addr = self.get_register_pair('hl')
        hlval = self.mmu.read_byte(addr)
        notval = ~(2 ** b)
        hlval = hlval & notval
        self.mmu.write_byte(addr, hlval)
        self.registers.m = 4


    #region RES_b_hl Shortcuts
    def RES_0_hl(self):
        self.RES_b_hl(0)

    def RES_1_hl(self):
        self.RES_b_hl(1)

    def RES_2_hl(self):
        self.RES_b_hl(2)

    def RES_3_hl(self):
        self.RES_b_hl(3)

    def RES_4_hl(self):
        self.RES_b_hl(4)

    def RES_5_hl(self):
        self.RES_b_hl(5)

    def RES_6_hl(self):
        self.RES_b_hl(6)

    def RES_7_hl(self):
        self.RES_b_hl(7)

        #endregion

    def JP_nn(self):
        ladrs = self.get_immediate_operand()
        hadrs = self.get_immediate_operand()
        addr = (hadrs << 8) + ladrs
        self.registers.pc = addr

    def JP_cc_nn(self, cc):
        ladrs = self.get_immediate_operand()
        hadrs = self.get_immediate_operand()
        addr = (hadrs << 8) + ladrs
        if cc == 'nz':
            if not self.flags.z:
                self.registers.pc = addr
                self.registers.m = 4
            else:
                self.registers.m = 3
        elif cc == 'z':
            if self.flags.z:
                self.registers.pc = addr
                self.registers.m = 4
            else:
                self.registers.m = 3
        elif cc == 'nc':
            if not self.flags.cy:
                self.registers.pc = addr
                self.registers.m = 4
            else:
                self.registers.m = 3
        elif cc == 'c':
            if self.flags.cy:
                self.registers.pc = addr
                self.registers.m = 4
            else:
                self.registers.m = 3

    def JP_nz_nn(self):
        self.JP_cc_nn('nz')

    def JP_z_nn(self):
        self.JP_cc_nn('z')

    def JP_nc_nn(self):
        self.JP_cc_nn('nc')

    def JP_c_nn(self):
        self.JP_cc_nn('c')

    def JR_e(self):
        value = self.get_immediate_operand()
        if value > 127:
            value = -((~value + 1) & 255)
        self.registers.pc += value
        self.registers.m = 3

    def JR_cc_e(self, cc):
        value = self.get_immediate_operand()
        if value > 127:
            value = -((~value + 1) & 255)
        self.registers.m = 2
        if cc == 'nz':
            if not self.flags.z:
                self.registers.pc += value
                self.registers.m += 1
        elif cc == 'z':
            if self.flags.z:
                self.registers.pc += value
                self.registers.m += 1
        elif cc == 'nc':
            if not self.flags.cy:
                self.registers.pc += value
                self.registers.m += 1
        elif cc == 'c':
            if self.flags.cy:
                self.registers.pc += value
                self.registers.m += 1

    def JR_nz_e(self):
        self.JR_cc_e('nz')

    def JR_z_e(self):
        self.JR_cc_e('z')

    def JR_nc_e(self):
        self.JR_cc_e('nc')

    def JR_c_e(self):
        self.JR_cc_e('c')

    def JP_hl(self):
        self.registers.pc = self.get_register_pair('hl')
        self.registers.m = 1

    def CALL_nn(self):
        ladrs = self.get_immediate_operand()
        hadrs = self.get_immediate_operand()
        nn = (hadrs << 8) + ladrs
        pch = self.registers.pc >> 8
        pcl = self.registers.pc & 0xFF
        self.mmu.write_byte(self.registers.sp - 1, pch)
        self.mmu.write_byte(self.registers.sp - 2, pcl)
        self.registers.pc = nn
        self.registers.sp -= 2
        self.registers.m = 6

    def CALL_cc_nn(self, cc):
        ladrs = self.get_immediate_operand()
        hadrs = self.get_immediate_operand()
        nn = (hadrs << 8) + ladrs
        passed = False
        if cc == 'nz':
            if not self.flags.z:
                passed = True
        elif cc == 'z':
            if self.flags.z:
                passed = True
        elif cc == 'nc':
            if not self.flags.cy:
                passed = True
        elif cc == 'c':
            if self.flags.cy:
                passed = True
        self.registers.m = 3
        if passed:
            pch = self.registers.pc >> 8
            pcl = self.registers.pc & 0xFF
            self.mmu.write_byte(self.registers.sp - 1, pch)
            self.mmu.write_byte(self.registers.sp - 2, pcl)
            self.registers.pc = nn
            self.registers.sp -= 2
            self.registers.m = 6

    def CALL_nz_nn(self):
        self.CALL_cc_nn('nz')

    def CALL_z_nn(self):
        self.CALL_cc_nn('z')

    def CALL_nc_nn(self):
        self.CALL_cc_nn('nc')

    def CALL_c_nn(self):
        self.CALL_cc_nn('c')

    def RET(self):
        self.registers.pc = self.mmu.read_word(self.registers.sp)
        self.registers.sp = self.registers.sp + 2
        self.registers.m = 4

    def RETI(self):
        #might be incorrect
        self.RET()

    def RET_cc(self, cc):
        passed = False
        if cc == 'nz':
            if not self.flags.z:
                passed = True
        elif cc == 'z':
            if self.flags.z:
                passed = True
        elif cc == 'nc':
            if not self.flags.cy:
                passed = True
        elif cc == 'c':
            if self.flags.cy:
                passed = True
        self.registers.m = 2
        if passed:
            self.RET()
            #RET will set it to 4 cycles, override
            self.registers.m = 5


    def RET_nz(self):
        self.RET_cc('nz')

    def RET_z(self):
        self.RET_cc('z')

    def RET_nc(self):
        self.RET_cc('nc')

    def RET_c(self):
        self.RET_cc('c')


    def RST_t(self, t):
        pch = self.registers.pc >> 8
        pcl = self.registers.pc & 0xFF
        self.mmu.write_byte(self.registers.sp - 1, pch)
        self.mmu.write_byte(self.registers.sp - 2, pcl)
        self.registers.sp -= 2
        self.registers.pc = t * 8
        self.registers.m = 4

    def RST_0(self):
        self.RST_t(0)

    def RST_1(self):
        self.RST_t(1)

    def RST_2(self):
        self.RST_t(2)

    def RST_3(self):
        self.RST_t(3)

    def RST_4(self):
        self.RST_t(4)

    def RST_5(self):
        self.RST_t(5)

    def RST_6(self):
        self.RST_t(6)

    def RST_7(self):
        self.RST_t(7)

    def DAA(self):
        a = self.registers.a
        hnibble = self.registers.a >> 8
        lnibble = self.registers.a & 0xFF
        self.registers.m = 1
        if not self.flags.n:
            #previous operation was ADD/ADC
            if not self.flags.cy:
                if hnibble <= 0x9:
                    if not self.flags.h:
                        if lnibble <= 0x9:
                            #line 1
                            return
                        else:
                            #line 2
                            self.registers.a += 0x06
                            self.registers.a &= 0xFF
                    else:
                        #line 3
                        self.registers.a += 0x06
                        self.registers.a &= 0xFF
                else:
                    if not self.flags.h:
                        if lnibble <= 0x9:
                            #line 4
                            self.registers.a += 0x60
                            self.registers.a &= 0xFF
                            self.flags.cy = True
                        else:
                            #line 5
                            self.registers.a += 0x66
                            self.registers.a &= 0xFF
                            self.flags.cy = True
                    else:
                        #line 6
                        self.registers.a += 0x66
                        self.registers.a &= 0xFF
                        self.flags.cy = True
            else:
                if not self.flags.h:
                    if lnibble <= 0x9:
                        #line 7
                        self.registers.a += 0x60
                        self.registers.a &= 0xFF
                        self.flags.cy = True
                    else:
                        #line 8
                        self.registers.a += 0x66
                        self.registers.a &= 0xFF
                        self.flags.cy = True
                else:
                    #line 9
                    self.registers.a += 0x66
                    self.registers.a &= 0xFF
                    self.flags.cy = True
        else:
            #Previous operation was SUB/SBC
            if not self.flags.cy:
                if not self.flags.h:
                    return
                else:
                    self.registers.a += 0xFA
                    self.registers.a &= 0xFF
                    self.flags.cy = False
            else:
                if not self.flags.h:
                    self.registers.a += 0xA0
                    self.registers.a &= 0xFF
                    self.flags.cy = True
                else:
                    self.registers.a += 0x9A
                    self.registers.a &= 0xFF
                    self.flags.cy = True

    def CPL(self):
        self.registers.a = self.registers.a ^ 0xFF
        self.registers.m = 1


    def NOP(self):
        self.registers.m = 1


    def HALT(self):
        self.halt = True
        self.registers.m = 1

    def STOP(self):
        self.stop = True
        self.registers.m = 1

    def NOTIMP(self):
        self.stop = True
        print "Unimplemented instruction %s Stopped" % hex(self.mmu.read_byte(self.registers.pc - 1))

    def create_map(self):
        map = [
        #00 |NOP|       LD BC,nn |      LD (BC),A |     INC BC    |         INC B      |DEC B    |  LD B,n    | RLCA     |
            self.NOP,   self.LDbc_nn,   self.LDbc_a,    self.INC_ss_bc,     self.INCb,  self.DECb,  self.LDb_n, self.RLCA,
        #08 |EX AF,AF | ADD HL,BC|      LD A,(BC) |     DEC BC    |         INC C      |DEC C    |  LD C,n    | RRCA     |
            self.NOTIMP,self.ADDhl_bc,  self.LDa_bc,    self.DEC_ss_bc,     self.INCc,  self.DECc,  self.LDc_n, self.RRCA,
        #10 |DJNZ d   | LD DE,nn |      LD (DE),A |     INC DE    |         INC D      |DEC D    |  LD D,n    | RLA      |
            self.NOTIMP,self.LDde_nn,   self.LDde_a,    self.INC_ss_de,     self.INCd,  self.DECd,  self.LDd_n, self.RLA,
        #18 |JR d     |ADD HL,DE|       LD A,(DE) |     DEC DE    |         INC E      |DEC E    |  LD E,n    | RRA      |
            self.JR_e,self.ADDhl_de,  self.LDa_de,      self.DEC_ss_de,     self.INCe,  self.DECe,  self.LDe_n, self.RRA,
        #20 |JR NZ,d  |LD HL,nn |       LD (nn),HL|     INC HL    |         INC H      |DEC H    |  LD H,n    | DAA      |
            self.JR_nz_e,self.LDhl_nn,  self.NOTIMP,    self.INC_ss_hl,     self.INCh,  self.DECh,  self.LDh_n, self.DAA,
        #28 |JR Z,d   |ADD HL,HL|       LD HL,(nn)|     DEC HL    |         INC L      |DEC L    |  LD L,n    | CPL      |
            self.JR_z_e,self.ADDhl_hl,  self.LDhl_nn,   self.DEC_ss_hl,     self.INCl, self.DECl,   self.LDl_n, self.CPL,
        #30 |JR NC,d  |LD SP,nn |       LD (nn),A |     INC SP    |         INC (HL)   |DEC (HL) |  LD (HL),n | SCF      |
            self.JR_nc_e(),self.LDsp_nn,self.LDnn_a,    self.INC_ss_sp,     self.INChl, self.DEChl,self.LDhl_n,self.NOTIMP,
        #38 |JR C,d   |ADD HL,SP|       LD A,(nn) |     DEC SP    |         INC A      |DEC A    |  LD A,n    | CCF      |
            self.JR_c_e,self.ADDhl_sp,  self.LDa_nn,    self.DEC_ss_sp,     self.INCa,  self.DECa,  self.LDa_n, self.NOTIMP,
        #40 |LD B,B   |LD B,C   |       LD B,D    |     LD B,E    |         LD B,H     |LD B,L   |  LD B,(HL) | LD B,A   |
            self.LDb_b,self.LDb_c,      self.LDb_d,     self.LDb_e,         self.LDb_h, self.LDb_l, self.LDb_hl,self.LDb_a,
        #48 |LD C,B   |LD C,C   |       LD C,D    |     LD C,E    |         LD C,H     |LD C,L   |  LD C,(HL) | LD C,A   |
            self.LDc_b,self.LDc_c,      self.LDc_d,     self.LDc_e,         self.LDc_h, self.LDc_l, self.LDc_hl,self.LDc_a,
        #50 |LD D,B   |LD D,C   |       LD D,D    |     LD D,E    |         LD D,H     |LD D,L   |  LD D,(HL) | LD D,A   |
            self.LDd_b,self.LDd_c,      self.LDd_d,     self.LDd_e,         self.LDd_h, self.LDd_l, self.LDd_hl,self.LDd_a,
        #58 |LD E,B   |LD E,C   |       LD E,D    |     LD E,E    |         LD E,H     |LD E,L   |  LD E,(HL) | LD E,A   |
            self.LDe_b,self.LDe_c,      self.LDe_d,     self.LDe_e,         self.LDe_h, self.LDe_l, self.LDe_hl,self.LDe_a,
        #60 |LD H,B   |LD H,C   |       LD H,D    |     LD H,E    |         LD H,H     |LD H,L   |  LD H,(HL) | LD H,A   |
            self.LDh_b,self.LDh_c,      self.LDh_d,     self.LDh_e,         self.LDh_h,self.LDh_l,  self.LDh_hl,self.LDh_a,
        #68 |LD L,B   |LD L,C   |       LD L,D    |     LD L,E    |         LD L,H     |LD L,L   |  LD L,(HL) | LD L,A   |
            self.LDl_b,self.LDl_c,      self.LDl_d,     self.LDl_e,         self.LDl_h,self.LDl_l,  self.LDl_hl,self.LDl_a,
        #70 |LD (HL),B|LD (HL),C|       LD (HL),D |     LD (HL),E |         LD (HL),H  |LD (HL),L|  HALT      | LD (HL),A|
            self.LDhl_b,self.LDhl_c,    self.LDhl_d,    self.LDhl_e,        self.LDhl_h,self.LDhl_l,self.HALT,  self.LDhl_a,
        #78 |LD A,B   |LD A,C   |       LD A,D    |     LD A,E    |         LD A,H     |LD A,L   |  LD A,(HL) | LD A,A   |
            self.LDa_b,self.LDa_c,      self.LDa_d,     self.LDa_e,         self.LDa_h, self.LDa_l, self.LDa_hl,self.LDa_a,

        ]


    def decode(self, b):
        pass