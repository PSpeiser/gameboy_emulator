class GPU(object):
    def __init__(self):
        self.vram = [0 for i in range(16384)] #16kb vram
        self.oam = []