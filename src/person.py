from utils import GameObject

class Worker(GameObject):
    def __init__(self, cell_size=100, position=(0, 0), picture='../res/worker.png', **kwargs):
        self.price = 1000
        self.pertime = 50
        self.income = 100

        super().__init__(picture, **kwargs)

        self.size = (cell_size, cell_size)

    def update(self):
        self.move(step=1)

    def move(self, step):
        self.pos = self.pos[0] + step, self.pos[1] + step