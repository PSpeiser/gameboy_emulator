import unittest
import gameboy_emulator

class TestCPUArithmetic(unittest.TestCase):
    def setUp(self):
        self.cpu = gameboy_emulator.CPU()

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
        self.gpu = gameboy_emulator.GPU()
        self.mmu = gameboy_emulator.MMU(self.gpu)

    def test_load_rom_file(self):
        self.mmu.load("Tetris.gb")


