from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty
)
from office import Office
from person import Worker
from kivy.core.audio import SoundLoader


class CorporationGame(FloatLayout):
    game_field = ObjectProperty(None)
    object_layer = ObjectProperty(None)
    worker_layer = ObjectProperty(None)

    gui = ObjectProperty(None)
    is_worker_opened = False
    is_office_opened = False

    money_display = None
    money = 1100

    time = 0
    salary_time = 15 * 60

    workers = []
    offices = []

    current_state = 'none'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self):
        self.game_field.fill_grass()

    def set_state(self, state):
        self.current_state = state

    def tick(self, dt):
        self.time += 1
        self.money_display.text = str(self.money)

        for worker in self.workers:
            worker.update()

            if self.time == self.salary_time:
                self.money -= worker.salary
                self.time = 0

    def place(self, pos):
        if self.current_state == 'worker':
            self.place_worker(pos)
            return

        if self.current_state == 'office':
            self.place_office(pos)
            return

    def add_money(self, money):
        self.money += money

    def remove_money(self, money):
        self.money -= money

    def place_worker(self, pos):
        if self.game_field.data[pos[1]][pos[0]].contains_office:
            w = Worker(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None),
                       office=self.game_field.data[pos[1]][pos[0]])
            self.worker_layer.add_widget(w)
            self.remove_money(w.price)
            self.workers.append(w)

    def place_office(self, pos):
        if self.game_field.can_be_placed(pos):
            o = Office(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None),
                       position=pos)
            self.remove_money(o.price)
            self.object_layer.add_widget(o)
            for i in range(6):
                self.game_field.data[pos[1]][pos[0] + i].contains_office = True

    def switch_state(self, state):
        if state == self.current_state:
            self.set_state('none')
            return

        self.set_state(state)
