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
        self.cpu.LDr_r('a','b')
        assert self.cpu.registers.a == self.cpu.registers.b

    def test_LDr_n(self):
        #set up cpu for immediate value
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000,0x24)
        #test the function
        self.cpu.LDr_n('a')
        #verify the result
        assert self.cpu.registers.a == 0x24

    def test_LDr_hl(self):
        self.cpu.registers.h = 0x20
        self.cpu.registers.l = 0x00
        self.mmu.write_byte(0x2000,0x5C)
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
        self.mmu.write_byte(0x1000,0xFF)

        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0xC5
        self.cpu.LDhl_n()
        assert self.mmu.read_byte(0x8AC5) == 0xFF

    def test_LDa_bc(self):
        self.cpu.registers.b = 0x8A
        self.cpu.registers.c = 0xC5
        self.mmu.write_byte(0x8AC5,0x2F)
        self.cpu.LDa_bc()
        assert self.cpu.registers.a == 0x2F

    def test_LDa_de(self):
        self.cpu.registers.d = 0x8A
        self.cpu.registers.e = 0xC5
        self.mmu.write_byte(0x8AC5,0x2F)
        self.cpu.LDa_de()
        assert self.cpu.registers.a == 0x2F

    def test_LDa_c(self):
        self.cpu.registers.c = 0x95
        self.mmu.write_byte(0xFF95,0xFF)
        self.cpu.LDa_c()
        assert self.cpu.registers.a == 0xFF

    def test_LDc_a(self):
        self.cpu.registers.a = 0xFF
        self.cpu.registers.c = 0x9F
        self.cpu.LDc_a()
        assert self.mmu.read_byte(0xFF9F) == 0xFF

    def test_LDa_n(self):
        #set up cpu for immediate value
        self.mmu.write_byte(0x1000,0x80)
        self.cpu.registers.pc = 0x1000

        self.mmu.write_byte(0xFF80,0xFF)
        self.cpu.LDa_n()
        assert self.cpu.registers.a == 0xFF

    def test_LDn_a(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_byte(0x1000,0x80)

        self.cpu.registers.a = 0xFF
        self.cpu.LDn_a()
        assert self.mmu.read_byte(0xFF80)
        assert self.cpu.registers.pc == 0x1001

    def test_LDa_nn(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000,0x8000)

        self.mmu.write_byte(0x8000,0xFF)
        self.cpu.LDa_nn()
        assert self.cpu.registers.a == 0xFF
        assert self.cpu.registers.pc == 0x1002

    def test_LDnn_a(self):
        self.cpu.registers.pc = 0x1000
        self.mmu.write_word(0x1000,0x8000)

        self.cpu.registers.a = 0xFF
        self.cpu.LDnn_a()
        assert self.mmu.read_byte(0x8000) == 0xFF

    def test_LDa_hli(self):
        self.mmu.write_byte(0x01FF,0x56)
        self.cpu.registers.h = 0x01
        self.cpu.registers.l = 0xFF
        self.cpu.LDa_hli()
        assert self.cpu.registers.h == 0x02
        assert self.cpu.registers.l == 0x00
        assert self.cpu.registers.a == 0x56

    def test_LDa_hld(self):
        self.mmu.write_byte(0x8A5C,0x3C)
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

    def test_LDbc_a(self):
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
        self.mmu.write_word(0x1000,0x3A5B)
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
        self.mmu.write_byte(0xFFFC,0x5F)
        self.mmu.write_byte(0xFFFD,0x3C)
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
        self.mmu.write_byte(0x1000,2)
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
        self.mmu.write_word(0x1000,0xC100)
        self.cpu.LDnn_sp()
        assert self.mmu.read_byte(0xC100) == 0xF8
        assert self.mmu.read_byte(0xC101) == 0xFF

    #endregion




class TestCPUArithmetic(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu

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
        self.cpu.registers.a = 0x3C
        self.cpu.ADDn(0xFF)
        assert self.cpu.registers.a == 0x3B
        assert self.cpu.flags.z == False
        assert self.cpu.flags.h == True
        assert self.cpu.flags.n == False
        assert self.cpu.flags.cy == True

class TestMMU(unittest.TestCase):
    def setUp(self):
        global gpu
        gpu = gameboy_emulator.gpu
        self.mmu = gameboy_emulator.mmu

    def test_load_rom_file(self):
        self.mmu.load("Tetris.gb")


