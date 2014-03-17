import unittest
import gameboy_emulator

class TestCPUIO(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.cpu
        self.mmu = gameboy_emulator.mmu

    def test_LDr_r(self):
        self.cpu.registers.a = 0x00
        self.cpu.registers.b = 0xFF
        self.cpu.LDr_r('a','b')
        assert self.cpu.registers.a == self.cpu.registers.b

    def test_LDr_n(self):
        self.cpu.LDr_n('a',0x24)
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
        self.cpu.registers.h = 0x8A
        self.cpu.registers.l = 0xC5
        self.cpu.LDhl_n(0xFF)
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


