import unittest
import gameboy_emulator


class TestCPUIO(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    #region 8-Bit Transfer and Input/Output Instructions
    def test_LDr_r(self):
        self.cpu.registers.a = 0x00
        self.cpu.registers.b = 0xFF
        self.cpu.LDr_r('a', 'b')
        assert self.cpu.registers.a == self.cpu.registers.b

    def test_LDr_n(self):
        #set up cpu for immediate value
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x24)
        #test the function
        self.cpu.LDr_n('a')
        #verify the result
        assert self.cpu.registers.a == 0x24

    def test_LDr_hl(self):
        self.cpu.registers.h = 0x20
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x2000, 0x5C)
        self.cpu.LDr_hl('a')
        assert self.cpu.registers.a == 0x5C

    def test_LDhl_r(self):
        self.cpu.registers.a = 0x3C
        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0xC5
        self.cpu.LDhl_r('a')
        assert self.mmu.read_byte(0x8AC5) == 0x3C

    def test_LDhl_n(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0xFF)

        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0xC5
        self.cpu.LDhl_n()
        assert self.mmu.read_byte(0x8AC5) == 0xFF

    def test_LDa_bc(self):
        self.cpu.registers.b = 0x8A
        self.cpu.registers.c = 0xC5
        self.mmu.write_byte(0x8AC5, 0x2F)
        self.cpu.LDa_bc()
        assert self.cpu.registers.a == 0x2F

    def test_LDa_de(self):
        self.cpu.registers.d = 0x8A
        self.cpu.registers.e = 0xC5
        self.mmu.write_byte(0x8AC5, 0x2F)
        self.cpu.LDa_de()
        assert self.cpu.registers.a == 0x2F

    def test_LDa_c(self):
        self.cpu.registers.c = 0x95
        self.mmu.write_byte(0xFF95, 0xFF)
        self.cpu.LDa_c()
        assert self.cpu.registers.a == 0xFF

    def test_LDc_a(self):
        self.cpu.registers.a = 0xFF
        self.cpu.registers.c = 0x9F
        self.cpu.LDc_a()
        assert self.mmu.read_byte(0xFF9F) == 0xFF

    def test_LDa_n(self):
        #set up cpu for immediate value
        self.mmu.write_byte(0x1000, 0x80)
        self.cpu.registers.pc = 0x1000

        self.mmu.write_byte(0xFF80, 0xFF)
        self.cpu.LDa_n()
        assert self.cpu.registers.a == 0xFF

    def test_LDn_a(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x80)

        self.cpu.registers.a = 0xFF
        self.cpu.LDn_a()
        assert self.mmu.read_byte(0xFF80)
        assert self.cpu.registers.pc == 0x1001

    def test_LDa_nn(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000, 0x8000)

        self.mmu.write_byte(0x8000, 0xFF)
        self.cpu.LDa_nn()
        assert self.cpu.registers.a == 0xFF
        assert self.cpu.registers.pc == 0x1002

    def test_LDnn_a(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000, 0x8000)

        self.cpu.registers.a = 0xFF
        self.cpu.LDnn_a()
        assert self.mmu.read_byte(0x8000) == 0xFF

    def test_LDa_hli(self):
        self.mmu.write_byte(0x01FF, 0x56)
        self.cpu.registers.h = 0x01
        self.cpu.registers.l = 0xFF
        self.cpu.LDa_hli()
        assert self.cpu.registers.h == 0x02
        assert self.cpu.registers.l == 0x00
        assert self.cpu.registers.a == 0x56

    def test_LDa_hld(self):
        self.mmu.write_byte(0x8A5C, 0x3C)
        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0x5C
        self.cpu.LDa_hld()
        assert self.cpu.registers.h == 0x8A
        assert self.cpu.registers.l == 0x5B
        assert self.cpu.registers.a == 0x3C

    def test_LDbc_a(self):
        self.cpu.registers.b = 0x20
        self.cpu.registers.c = 0x5F
        self.cpu.registers.a = 0x3F
        self.cpu.LDbc_a()
        assert self.mmu.read_byte(0x205F) == 0x3F

    def test_LDde_a(self):
        self.cpu.registers.d = 0x20
        self.cpu.registers.e = 0x5C
        self.cpu.registers.a = 0xFF
        self.cpu.LDde_a()
        assert self.mmu.read_byte(0x205C) == 0xFF

    def test_LDhli_a(self):
        self.cpu.registers.h = 0xFF
        self.cpu.registers.l = 0xFF
        self.cpu.registers.a = 0x56
        self.cpu.LDhli_a()
        assert self.mmu.read_byte(0xFFFF) == 0x56
        assert self.cpu.registers.h == 0x00
        assert self.cpu.registers.l == 0x00

    def test_LDhld_a(self):
        self.cpu.registers.h = 0x40
        self.cpu.registers.l = 0x00
        self.cpu.registers.a = 0x05
        self.cpu.LDhld_a()
        assert self.mmu.read_byte(0x4000) == 0x05
        assert self.cpu.registers.h == 0x3F
        assert self.cpu.registers.l == 0xFF

    #endregion

    #region 16-Bit Transfer Instructions
    def test_LDdd_nn(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000, 0x3A5B)
        self.cpu.LDdd_nn('hl')
        assert self.cpu.registers.h == 0x3A
        assert self.cpu.registers.l == 0x5b
        assert self.cpu.registers.pc == 0x1002

    def test_LDsp_hl(self):
        self.cpu.registers.h = 0xFF
        self.cpu.registers.l = 0xFF
        self.cpu.LDsp_hl()
        assert self.cpu.registers.sp == 0xFFFF

    def test_PUSH_qq(self):
        self.cpu.registers.sp = 0xFFFE
        self.cpu.registers.b = 0x12
        self.cpu.registers.c = 0x34
        self.cpu.PUSH_qq('bc')
        assert self.mmu.read_word(0xFFFC) == 0x1234
        assert self.cpu.registers.sp == 0xFFFC

    def test_POP_qq(self):
        self.cpu.registers.sp = 0xFFFC
        self.mmu.write_byte(0xFFFC, 0x5F)
        self.mmu.write_byte(0xFFFD, 0x3C)
        self.cpu.POP_qq('bc')
        assert self.cpu.registers.b == 0x3C
        assert self.cpu.registers.c == 0x5F
        assert self.cpu.registers.sp == 0xFFFE

    def test_PUSH_POP(self):
        self.cpu.registers.sp = 0xFFFE
        self.cpu.registers.b = 0x12
        self.cpu.registers.c = 0x34
        self.cpu.PUSH_qq('bc')
        self.cpu.POP_qq('de')
        assert self.cpu.registers.d == self.cpu.registers.b
        assert self.cpu.registers.e == self.cpu.registers.c
        assert self.cpu.registers.sp == 0xFFFE

    def test_LDHLsp_e(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 2)
        self.cpu.registers.sp = 0xFFF8
        self.cpu.LDHLsp_e()
        assert self.cpu.registers.h == 0xFF
        assert self.cpu.registers.l == 0xFA
        assert self.cpu.flags.cy == 0
        assert self.cpu.flags.h == 0
        assert self.cpu.flags.n == 0
        assert self.cpu.flags.z == 0

    def test_LDnn_sp(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000, 0xC100)
        self.cpu.LDnn_sp()
        assert self.mmu.read_byte(0xC100) == 0xF8
        assert self.mmu.read_byte(0xC101) == 0xFF

        #endregion


class TestCPUArithmetic(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_ADDr_example(self):
        self.cpu.registers.a = 0x3A
        self.cpu.registers.b = 0xC6
        self.cpu.ADDr('b')
        assert self.cpu.registers.a == 0
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == True

    def test_ADDr_normal(self):
        self.cpu.registers.a = 200
        self.cpu.registers.b = 50
        self.cpu.ADDr('b')
        assert self.cpu.registers.a == 250
        assert self.cpu.flags.z == False
        assert self.cpu.flags.n == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.cy == False

    def test_ADDr_overflow(self):
        self.cpu.registers.a = 255
        self.cpu.registers.b = 1
        self.cpu.ADDr('b')
        assert self.cpu.registers.a == 0
        assert self.cpu.flags.z == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.cy == True

    def test_ADDr_zero(self):
        self.cpu.registers.a = 0
        self.cpu.registers.b = 0
        self.cpu.ADDr('b')
        assert self.cpu.registers.a == 0
        assert self.cpu.flags.z == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.cy == False

    def test_ADDn_example(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0xFF)
        self.cpu.registers.a = 0x3C
        self.cpu.ADDn()
        assert self.cpu.registers.a == 0x3B
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == True

    def test_ADDa_hl(self):
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x12)
        self.cpu.registers.a = 0x3C
        self.cpu.ADDa_hl()
        assert self.cpu.registers.a == 0x4E
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == False

    def test_ADCa_r(self):
        self.cpu.registers.a = 0xE1
        self.cpu.registers.e = 0x0F
        self.cpu.flags.cy = True
        self.cpu.ADCa_r('e')
        assert self.cpu.registers.a == 0xF1
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.cy == False

    def test_ADCa_n(self):
        self.cpu.registers.a = 0xE1
        self.cpu.flags.cy = True
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x3B)
        self.cpu.ADCa_n()
        assert self.cpu.registers.a == 0x1D
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.cy == True


    def test_ADCa_hl(self):
        self.cpu.registers.a = 0xE1
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x1E)
        self.cpu.flags.cy = True
        self.cpu.ADCa_hl()
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.cy == True

    def test_SUBr(self):
        self.cpu.registers.a = 0x3E
        self.cpu.registers.e = 0x3E
        self.cpu.SUBr('e')
        assert self.cpu.registers.a == 0
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_SUBr_halfcarry(self):
        self.cpu.registers.a = 0x10
        self.cpu.registers.b = 0x01
        self.cpu.SUBr('b')
        assert self.cpu.registers.a == 0x0F
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_SUBr_carry(self):
        self.cpu.registers.a = 0x00
        self.cpu.registers.b = 0x01
        self.cpu.SUBr('b')
        assert self.cpu.registers.a == 0xFF
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == True

    def test_SUBn(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x0F)
        self.cpu.registers.a = 0x3E
        self.cpu.SUBn()
        assert self.cpu.registers.a == 0x2F
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_SUBhl(self):
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x40)
        self.cpu.registers.a = 0x3E
        self.cpu.SUBhl()
        assert self.cpu.registers.a == 0xFE
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == True

    def test_SBCa_r(self):
        self.cpu.registers.h = 0x2A
        self.cpu.registers.a = 0x3B
        self.cpu.flags.cy = True
        self.cpu.SBCa_r('h')
        assert self.cpu.registers.a == 0x10
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_SBCa_n(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x3A)
        self.cpu.registers.a = 0x3B
        self.cpu.flags.cy = True
        self.cpu.SBCa_n()
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_SBCa_hl(self):
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x4F)
        self.cpu.registers.a = 0x3B
        self.cpu.flags.cy = True
        self.cpu.SBCa_hl()
        assert self.cpu.registers.a == 0xEB
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == True

    def test_ANDr(self):
        self.cpu.registers.a = 0x5A
        self.cpu.registers.l = 0x3F
        self.cpu.ANDr('l')
        assert self.cpu.registers.a == 0x1A
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == False

    def test_ANDn(self):
        self.cpu.registers.a = 0x5A
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x38)
        self.cpu.ANDn()
        assert self.cpu.registers.a == 0x18
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == False

    def test_ANDhl(self):
        self.cpu.registers.a = 0x5A
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x00)
        self.cpu.ANDhl()
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == False

    def test_ORr(self):
        self.cpu.registers.a = 0x5A
        self.cpu.ORr('a')
        assert self.cpu.registers.a == 0x5A
        assert self.cpu.flags.z == False

    def test_ORn(self):
        self.cpu.registers.a = 0x5A
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x03)
        self.cpu.ORn()
        assert self.cpu.registers.a == 0x5B
        assert self.cpu.flags.z == False

    def test_ORhl(self):
        self.cpu.registers.a = 0x5A
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x0F)
        self.cpu.ORhl()
        assert self.cpu.registers.a == 0x5F
        assert self.cpu.flags.z == False

    def test_XORr(self):
        self.cpu.registers.a = 0xFF
        self.cpu.XORr('a')
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.z == True

    def test_XORn(self):
        self.cpu.registers.a = 0xFF
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x0F)
        self.cpu.XORn()
        assert self.cpu.registers.a == 0xF0
        assert self.cpu.flags.z == False

    def test_XORhl(self):
        self.cpu.registers.a = 0xFF
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x8A)
        self.cpu.XORhl()
        assert self.cpu.registers.a == 0x75
        assert self.cpu.flags.z == False

    def test_CPr(self):
        self.cpu.registers.a = 0x3C
        self.cpu.registers.b = 0x2F
        self.cpu.CPr('b')
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_CPn(self):
        self.cpu.registers.a = 0x3C
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x3C)
        self.cpu.CPn()
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == False

    def test_CPhl(self):
        self.cpu.registers.a = 0x3C
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x40)
        self.cpu.CPhl()
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True
        assert self.cpu.flags.cy == True

    def test_INCr(self):
        self.cpu.registers.a = 0xFF
        self.cpu.INCr('a')
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False

    def test_INChl(self):
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x50)
        self.cpu.INChl()
        assert self.mmu.read_byte(0x8000) == 0x51
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_DECr(self):
        self.cpu.registers.l = 0x01
        self.cpu.DECr('l')
        assert self.cpu.registers.l == 0x00
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == True

    def test_DEChl(self):
        self.cpu.registers.h = 0x80
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x8000, 0x00)
        self.cpu.DEChl()
        assert self.mmu.read_byte(0x8000) == 0xFF
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == True

    def test_ADDhl_ss(self):
        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0x23
        self.cpu.registers.b = 0x06
        self.cpu.registers.c = 0x05
        self.cpu.ADDhl_ss('bc')
        assert self.cpu.registers.h == 0x90
        assert self.cpu.registers.l == 0x28
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == False

    def test_ADDhl_ss2(self):
        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0x23
        self.cpu.ADDhl_ss('hl')
        assert self.cpu.registers.h == 0x14
        assert self.cpu.registers.l == 0x46
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == True

    def test_ADDsp_e(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000, 0x02)
        self.cpu.registers.sp = 0xFFF8
        self.cpu.ADDsp_e()
        assert self.cpu.registers.sp == 0xFFFA
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False
        assert self.cpu.flags.z == False

    def test_INC_ss(self):
        self.cpu.set_register_pair('de', 0x235F)
        self.cpu.INC_ss('de')
        assert self.cpu.get_register_pair('de') == 0x2360

    def test_DEC_ss(self):
        self.cpu.set_register_pair('de', 0x235F)
        self.cpu.DEC_ss('de')
        assert self.cpu.get_register_pair('de') == 0x235E


class TestCPULogicalOperations(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_RLCA(self):
        self.cpu.registers.a = 0x85
        self.cpu.flags.cy = False
        self.cpu.RLCA()
        assert self.cpu.registers.a == 0x0A
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RLA(self):
        self.cpu.registers.a = 0x95
        self.cpu.flags.cy = True
        self.cpu.RLA()
        assert self.cpu.registers.a == 0x2B
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RRCA(self):
        self.cpu.registers.a = 0x3B
        self.cpu.flags.cy = False
        self.cpu.RRCA()
        assert self.cpu.registers.a == 0x9D
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RRA(self):
        self.cpu.registers.a = 0x81
        self.cpu.flags.cy = False
        self.cpu.RRA()
        assert self.cpu.registers.a == 0x40
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RLC_r(self):
        self.cpu.registers.b = 0x85
        self.cpu.flags.cy = False
        self.cpu.RLC_r('b')
        assert self.cpu.registers.b == 0x0B
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RLC_hl(self):
        self.cpu.set_register_pair('hl', 0x8000)
        self.mmu.write_byte(0x8000, 0x00)
        self.cpu.flags.cy = False
        self.cpu.RLC_hl()
        assert self.mmu.read_byte(0x8000) == 0x00
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RL_r(self):
        self.cpu.registers.l = 0x80
        self.cpu.flags.cy = False
        self.cpu.RL_r('l')
        assert self.cpu.registers.l == 0x00
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RL_hl(self):
        self.cpu.set_register_pair('hl', 0x8000)
        self.mmu.write_byte(0x8000, 0x11)
        self.cpu.flags.cy = False
        self.cpu.RL_hl()
        assert self.mmu.read_byte(0x8000) == 0x22
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RRC_r(self):
        self.cpu.registers.c = 0x01
        self.cpu.flags.cy = False
        self.cpu.RRC_r('c')
        assert self.cpu.registers.c == 0x80
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RRC_hl(self):
        self.cpu.set_register_pair('hl', 0x8000)
        self.mmu.write_byte(0x8000, 0x00)
        self.cpu.flags.cy = False
        self.cpu.RRC_hl()
        assert self.mmu.read_byte(0x8000) == 0x00
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RR_r(self):
        self.cpu.registers.a = 0x01
        self.cpu.flags.cy = False
        self.cpu.RR_r('a')
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_RR_hl(self):
        self.cpu.set_register_pair('hl', 0x8000)
        self.mmu.write_byte(0x8000, 0x8A)
        self.cpu.flags.cy = False
        self.cpu.RR_hl()
        assert self.mmu.read_byte(0x8000) == 0x45
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SLA_r(self):
        self.cpu.registers.d = 0x80
        self.cpu.flags.cy = False
        self.cpu.SLA_r('d')
        assert self.cpu.registers.d == 0x00
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SLA_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0xFF)
        self.cpu.flags.cy = False
        self.cpu.SLA_hl()
        assert self.mmu.read_byte(0x8000) == 0xFE
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SRA_r(self):
        self.cpu.registers.a = 0x8A
        self.cpu.flags.cy = False
        self.cpu.SRA_r('a')
        assert self.cpu.registers.a == 0xC5
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SRA_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0x01)
        self.cpu.flags.cy = False
        self.cpu.SRA_hl()
        assert self.mmu.read_byte(0x8000) == 0x00
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SRL_r(self):
        self.cpu.registers.a = 0x01
        self.cpu.flags.cy = False
        self.cpu.SRL_r('a')
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SRL_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0xFF)
        self.cpu.flags.cy = False
        self.cpu.SRL_hl()
        assert self.mmu.read_byte(0x8000) == 0x7F
        assert self.cpu.flags.cy == True
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SWAP_r(self):
        self.cpu.registers.a = 0x00
        self.cpu.SWAP_r('a')
        assert self.cpu.registers.a == 0x00
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

        self.cpu.registers.a = 0x0F
        self.cpu.SWAP_r('a')
        assert self.cpu.registers.a == 0xF0
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

    def test_SWAP_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0xF0)
        self.cpu.SWAP_hl()
        assert self.mmu.read_byte(0x8000) == 0x0F
        assert self.cpu.flags.cy == False
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == False
        assert self.cpu.flags.n == False

class TestCPUBitOperations(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_BITb_r(self):
        self.cpu.registers.a = 0x80
        self.cpu.BIT_7_a()
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        self.cpu.registers.l = 0xEF
        self.cpu.BIT_4_l()
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False

    def test_BIT_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0xFE)
        self.cpu.BIT_0_hl()
        assert self.cpu.flags.z == True
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        self.cpu.BIT_1_hl()
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False

    def test_SET_b_r(self):
        self.cpu.registers.a = 0x80
        self.cpu.SET_3_a()
        assert self.cpu.registers.a == 0x88 #example says this value should be 0x84, calculator says 0x88 is correct
        self.cpu.registers.l = 0x3B
        self.cpu.SET_7_l()
        assert self.cpu.registers.l == 0xBB

    def test_SET_b_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0x00)
        self.cpu.SET_3_hl()
        assert self.mmu.read_byte(self.cpu.get_register_pair('hl')) == 0x08 #example says this should be 04H[sic]

    def test_RES_b_r(self):
        self.cpu.registers.a = 0x80
        self.cpu.RES_7_a()
        assert self.cpu.registers.a == 0x00
        self.cpu.registers.l = 0x3B
        self.cpu.RES_1_l()
        assert self.cpu.registers.l == 0x39

    def test_RES_b_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.mmu.write_byte(0x8000,0xFF)
        self.cpu.RES_3_hl()
        assert self.mmu.read_byte(self.cpu.get_register_pair('hl')) == 0xF7

class TestJumpInstructions(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_JP_nn(self):
        self.mmu.write_byte(0x1000,0x00)
        self.mmu.write_byte(0x1001,0x80)
        self.cpu.registers.pc = 0x1000
        self.cpu.JP_nn()
        assert self.cpu.registers.pc == 0x8000

    def test_JP_cc_nn(self):
        self.cpu.flags.z = True
        self.cpu.flags.c = False
        self.mmu.write_byte(0x1000,0x00)
        self.mmu.write_byte(0x1001,0x80)
        self.cpu.registers.pc = 0x1000
        self.cpu.JP_nz_nn()
        assert self.cpu.registers.pc == 0x1002
        assert self.cpu.registers.m == 3

        self.cpu.registers.pc = 0x1000
        self.cpu.JP_z_nn()
        assert self.cpu.registers.pc == 0x8000
        assert self.cpu.registers.m == 4

        self.cpu.registers.pc = 0x1000
        self.cpu.JP_c_nn()
        assert self.cpu.registers.pc == 0x1002
        assert self.cpu.registers.m == 3

        self.cpu.registers.pc = 0x1000
        self.cpu.JP_nc_nn()
        assert self.cpu.registers.pc == 0x8000
        assert self.cpu.registers.m == 4

    def test_JR_e(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000,5)
        self.cpu.JR_e()
        assert self.cpu.registers.pc == 0x1006

    def test_JR_cc_e(self):
        self.mmu.write_byte(0x1000,5)

        self.cpu.registers.pc = 0x1000
        self.cpu.flags.z = False
        self.cpu.JR_nz_e()
        assert self.cpu.registers.pc == 0x1006

        self.cpu.registers.pc = 0x1000
        self.cpu.flags.z = True
        self.cpu.JR_nz_e()
        assert self.cpu.registers.pc == 0x1001

        self.mmu.write_byte(0x1000,0x80)
        self.cpu.registers.pc = 0x1000
        self.cpu.flags.z = True
        self.cpu.JR_z_e()
        assert self.cpu.registers.pc == 0x0F81

    def test_JP_hl(self):
        self.cpu.set_register_pair('hl',0x8000)
        self.cpu.JP_hl()
        assert self.cpu.registers.pc == 0x8000

class TestCallAndReturnInstructions(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_CALL(self):
        #CALL opcode was read from 0x8000
        self.cpu.registers.pc = 0x8001
        self.cpu.registers.sp = 0xFFFE
        self.mmu.write_word(0x8001,0x1234)
        self.cpu.CALL_nn()
        assert self.cpu.registers.pc == 0x1234
        assert self.mmu.read_byte(0xFFFD) == 0x80
        assert self.mmu.read_byte(0xFFFC) == 0x03

    def test_CALL_cc_nn(self):
        #CALL NZ, 0x1234
        self.mmu.write_byte(0x7FFD,0b1100100) #programming manual says the address should be 0x7FFC, i disagree
        self.mmu.write_word(0x7FFE,0x1234) #this will make the final byte end up at 0x7FFF, 0x7FFC would have caused a gap
        #CALL Z 0x1234
        self.mmu.write_byte(0x8000,0b1101100)
        self.mmu.write_word(0x8001,0x1234)
        self.cpu.registers.pc = 0x7FFD
        self.cpu.registers.sp = 0xFFFE
        self.cpu.flags.z = True
        #simulate fetch
        self.cpu.registers.pc += 1
        #CALL will increment pc by 2
        self.cpu.CALL_nz_nn()
        assert self.cpu.registers.pc == 0x8000
        #first instruction finished, should have been equivalent to NOP
        #simulate fetch
        self.cpu.registers.pc += 1
        self.cpu.CALL_z_nn()
        assert self.cpu.registers.pc == 0x1234
        assert self.mmu.read_byte(0xFFFD) == 0x80
        assert self.mmu.read_byte(0xFFFC) == 0x03

    def test_RET(self):
        #CALL 0x9000
        self.mmu.write_byte(0x8000,0b11001101)
        self.mmu.write_word(0x8001,0x9000)
        #RET
        self.mmu.write_byte(0x9000,0b11001001)
        #prepare registers
        self.cpu.registers.pc = 0x8000
        self.cpu.registers.sp = 0xFFFE
        #simulate fetch
        self.cpu.registers.pc += 1
        #verify that CALL works
        self.cpu.CALL_nn()
        assert self.cpu.registers.pc == 0x9000
        self.cpu.RET()
        assert self.cpu.registers.pc == 0x8003

    def test_RST(self):
        self.cpu.registers.pc = 0x8001
        self.cpu.registers.sp = 0xFFFE
        self.cpu.RST_1()
        assert self.cpu.registers.pc == 0x0008
        assert self.mmu.read_word(0xFFFC) == 0x8001





class TestMMU(unittest.TestCase):
    def setUp(self):
        global gpu
        gpu = gameboy_emulator.gpu
        self.mmu = gameboy_emulator.mmu

    def test_load_rom_file(self):
        self.mmu.load("Tetris.gb")


