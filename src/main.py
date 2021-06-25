from abc import ABC, abstractmethod, ABCMeta
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.graphics.instructions import Canvas
from kivy.properties import (
    ObjectProperty, BooleanProperty, NumericProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.widget import Widget


class Utils:
    @staticmethod
    def get_rectangle(filename="ground.png", pos=(0, 0), size=(100, 100)):
        texture = Image(source=filename).texture
        texture.mag_filter = 'nearest'
        return Rectangle(texture=texture, size=size, pos=pos)


class GameObject(Button):
    def __init__(self, picture='air.png', cell_size=100, position=(-1, -1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = picture
        self.background_down = self.background_normal

        if position != (-1, -1):
            self.pos = get_game().game_field.get_pos(position)


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


class Office(GameObject):
    def __init__(self, cell_size=100, position=(0, 0), picture='../res/office.png', **kwargs):
        self.price = 1000
        self.pertime = 50
        self.capacity = 4
        self.reliability = 1000
        self.breakdown = 15
        self.income = 100

        super().__init__(picture, **kwargs)

        self.size = (6 * cell_size, cell_size)

    def update(self):
        self.reliability -= self.breakdown

    def repair(self):
        self.reliability = (self.reliability + self.breakdown * 4) % 1000


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


class Worker:
    def __init__(self, pos=(0, 0), source='worker.png', size=(100, 100), id=0, rectangle=None, n=0):
        self.pos = pos
        self.source = source
        self.size = size
        self.id = id
        self.rectangle = rectangle
        self.parent_n = n
        self.dx = 0

    def update_rectangle(self):
        self.rectangle = Utils.get_rectangle(filename=self.source, size=self.size, pos=self.pos)
        return self.rectangle

    def update_parent_n(self):
        if self.dx == 100:
            self.parent_n += 1
            self.dx = 0

    def update(self):
        self.move(1)

    def move(self, x):
        get_game().game_field.data[self.parent_n]['canvas'].remove(self.rectangle)

        x0, y0 = self.pos
        self.pos = (x + x0, y0)

        self.update_rectangle()

        self.dx += x
        self.update_parent_n()

        get_game().game_field.data[self.parent_n]['canvas'].add(self.rectangle)


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
        if n >= (self.game_field.h - 1) * self.game_field.w:
            return

        cur_cell = self.game_field.data[n]
        if cur_cell['contains_office']:
            w = Worker(pos=pos, id=len(self.workers) + 1, n=n)
            self.workers.append(w)
            self.money -= 100
            cur_cell['canvas'].add(w.update_rectangle())

    def place_office(self, pos):
        if self.game_field.can_be_placed(pos):
            self.object_layer.\
                add_widget(Office(pos=self.game_field.get_pos(pos),
                                  cell_size=self.game_field.cell_size,
                                  size_hint=(None, None)))
            for i in range(6):
                self.game_field.data[pos[1]][pos[0] + i].contains_office = True


def get_game():
    return CorporationApp.get_running_app().game


def switch_state(instance):
    if instance.text == get_game().current_state:
        get_game().set_state('none')
        return

    get_game().set_state(instance.text)

    if get_game().current_state != 'office':
        if get_game().is_office_being_built:
            k = 0
            for i in get_game().office_buffer:
                get_game().game_field.data[i]['canvas'].remove(get_game().office_texture_buffer[k])
                k += 1
            get_game().is_office_being_built = False

        get_game().clear_office_buffer()


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
