from person import Person, Status
from utils import GameObject, get_game


class Worker(GameObject, Person):
    def __init__(self, cell_size=100, position=(0, 0), office=None, picture='worker.png', **kwargs):
        self.price = 100
        self.salary = 600
        self.income = 2
        self.status = Status.WORKING
        self.fatigue = 0
        self.toilet = 0
        self.office = office
        self.working_pos = None

        super().__init__(picture, **kwargs)

        self.working_pos = (self.pos[0], self.pos[1])
        self.size = (cell_size, cell_size)

    def update(self):
        if self.status == Status.WORKING:
            self.fatigue += 1
            if self.office.is_broken():
                get_game().add_money(self.income // 2)
            else:
                get_game().add_money(self.income)

        if self.status != Status.RESTING and self.status != Status.TOILET and self.fatigue > 10 * 60:
            self.status = Status.RESTING

        if self.status == Status.RESTING:
            if self.fatigue > 0:
                self.fatigue -= 3
            self.move_rest()

        if self.fatigue <= 0 and self.status != Status.WORKING and self.status != Status.GOING_TO_WORK:
            self.status = self.status.GOING_TO_WORK

        if self.status == Status.GOING_TO_WORK:
            if self.pos[0] != self.working_pos[0]:
                self.move_work()
            else:
                self.status = Status.WORKING

    def move_work(self):
        if self.pos[0] < self.working_pos[0]:
            self.move(1)
        else:
            self.move(-1)

    def move_rest(self):
        if self.pos[0] + self.width < self.office.pos[0] + self.office.width:
            self.move(1)

    def move(self, step):
        self.pos = self.pos[0] + step, self.pos[1]

    def on_press(self):
        print(self.status, self.fatigue)
