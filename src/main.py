from abc import ABC, abstractmethod, ABCMeta

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import (
    ObjectProperty
)
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from utils import GameObject, get_game
from office import Office
from person import Worker

class MyMeta(ABCMeta, type(GameObject)):
    pass


class Room(ABC, metaclass=MyMeta):
    def __init__(self):
        self.price
        self.pertime
        self.capacity
        self.reliability
        self.breakdown
        self.income

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def repair(self):
        pass


class Cell(GameObject):
    def __init__(self, position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.position = position
        self.contains_office = False

    def on_press(self):
        print(self.position)
        get_game().place(self.position)


class Grass(GameObject):
    def __init__(self, picture='../res/ground.png', cell_size=100, **kwargs):
        super().__init__(picture, **kwargs)
        self.size = (cell_size, cell_size)


class GameField(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.h, self.w = 10, 20
        self.cell_size = Window.height / self.h

        self.data = [[Cell(position=(x, y),
                           height=self.cell_size,
                           width=self.cell_size,
                           size_hint=(None, None))
                      for x in range(self.w)] for y in range(self.h)]

        for i in self.data:
            for j in i:
                self.add_widget(j)

    def fill_grass(self):
        self.create_grass(first_pos=(0, self.h - 1), second_pos=(self.w - 1, self.h - 1))

    def create_grass(self, first_pos, second_pos):
        x = first_pos[0]
        while x != second_pos[0]:
            get_game() \
                .object_layer \
                .add_widget(Grass(pos=self.get_pos((x, second_pos[1])),
                                  size_hint=(None, None), cell_size=self.cell_size,
                                  ))
            x += 1

    def can_be_placed(self, pos):
        for i in range(6):
            print(pos[0] + i, pos[1])
            if self.data[pos[1]][pos[0] + i].contains_office:
                return False

        if pos[1] == self.h - 2:
            return True

        flag = False
        for i in range(6):
            if self.data[pos[1] + 1][pos[0] + i].contains_office:
                flag = True

        return flag

    def get_pos(self, pos):
        x, y = pos
        return x * self.cell_size, (self.h - 1 - y) * self.cell_size


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


def switch_state(instance):
    if instance.text == get_game().current_state:
        get_game().set_state('none')
        return

    get_game().set_state(instance.text)


class CorporationApp(App):
    game = None

    def build(self):
        self.game = CorporationGame()
        self.game.prepare()
        self.load_gui()
        Clock.schedule_interval(self.game.tick, 1.0 / 60.0)
        return self.game

    def load_gui(self):
        build_office = Button(text='office', size_hint=(.2, .2), pos_hint={'x': .01, 'y': .79})
        build_worker = Button(text='worker', size_hint=(.2, .2), pos_hint={'x': .22, 'y': .79})
        money_display = Button(text=str(get_game().money), size_hint=(.2, .2), pos_hint={'x': .79, 'y': .79})

        get_game().money_display = money_display

        build_worker.bind(on_press=switch_state)
        build_office.bind(on_press=switch_state)

        gui = get_game().gui
        gui.add_widget(build_office)
        gui.add_widget(build_worker)
        gui.add_widget(money_display)


if __name__ == '__main__':
    CorporationApp().run()
