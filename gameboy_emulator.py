from collections import namedtuple

from cpu import CPU
from mmu import MMU
from gpu import GPU

cpu = CPU()
gpu = GPU()
mmu = MMU()
cpu.mmu = mmu

