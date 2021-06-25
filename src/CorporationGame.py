from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty
)
from office import Office
from person import Worker

class CorporationGame(FloatLayout):
    game_field = ObjectProperty(None)
    object_layer = ObjectProperty(None)
    worker_layer = ObjectProperty(None)
    gui = ObjectProperty(None)

    money_display = None
    money = 0

    workers = []
    offices = []

    office_texture_buffer = []
    overlay_buffer = []
    office_buffer = []
    is_office_being_built = False

    current_state = 'none'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self):
        self.game_field.fill_grass()

    def set_state(self, state):
        self.current_state = state

    def tick(self, dt):
        self.money_display.text = str(self.money)

        for worker in self.workers:
            worker.update()

    def place(self, pos):
        if self.current_state == 'worker':
            self.place_worker(pos)
            return

        if self.current_state == 'office':
            self.place_office(pos)
            return

    def place_worker(self, pos):
        if self.game_field.data[pos[1]][pos[0]].contains_office:
            w = Worker(pos=self.game_field.get_pos(pos),
                       cell_size=self.game_field.cell_size,
                       size_hint=(None, None))
            self.worker_layer.add_widget(w)
            self.workers.append(w)

    def place_office(self, pos):
        if self.game_field.can_be_placed(pos):
            self.object_layer.\
                add_widget(Office(pos=self.game_field.get_pos(pos),
                                  cell_size=self.game_field.cell_size,
                                  size_hint=(None, None),
                                  position=pos))
            for i in range(6):
                self.game_field.data[pos[1]][pos[0] + i].contains_office = True
