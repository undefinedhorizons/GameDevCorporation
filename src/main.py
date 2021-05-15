from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.graphics.instructions import Canvas
from kivy.properties import (
    ObjectProperty, BooleanProperty, NumericProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView


class CorporationUtils:
    @staticmethod
    def rectangle_from_image(filename="ground.png", pos=(0, 0), size=(100, 100)):
        texture = Image(source=filename).texture
        texture.mag_filter = 'nearest'
        return Rectangle(texture=texture, size=size, pos=pos)


class Cell(Button):

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        self.position = None
        self.number = None
        self.contains_office = None
        self.office_texture = None
        self.overlay = None

    def on_press(self):
        get_game().place(self.position, self.number)


class GameField(RecycleView):

    def __init__(self, **kwargs):
        super(GameField, self).__init__(**kwargs)

        self.h, self.w = 10, 20

        self.cell_size = 100
        self.data = [{'canvas': Canvas(),
                      'position': (x % self.w * self.cell_size,
                                   (self.h - 1) * self.cell_size - x // self.w * self.cell_size),
                      'number': x,
                      'contains_office': False,
                      'workers': []}
                     for x in range(self.h * self.w)]

        self.fill((self.h - 1) * self.w, self.h * self.w, 'ground.png')

    def fill(self, first_pos, second_pos, filename):
        for i in range(first_pos, second_pos):
            ground = CorporationUtils. \
                rectangle_from_image(filename=filename,
                                     size=(self.cell_size, self.cell_size),
                                     pos=(i % self.w * self.cell_size,
                                          (self.h - 1) * self.cell_size - i // self.w * self.cell_size))
            self.data[i]['canvas'].add(ground)


class Worker:
    def __init__(self, pos=(0, 0), source='worker.png', size=(100, 100), id=0, rectangle=None):
        self.pos = pos
        self.source = source
        self.size = size
        self.id = id
        self.rectangle = rectangle

    def update_rectangle(self):
        self.rectangle = CorporationUtils.rectangle_from_image(filename=self.source, size=self.size, pos=self.pos)
        return self.rectangle


class CorporationGame(BoxLayout):
    game_field = ObjectProperty(None)
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
        super(CorporationGame, self).__init__(**kwargs)

    def set_state(self, state):
        self.current_state = state

    def tick(self, dt):
        self.money_display.text = str(self.money)

        # for worker in self.workers:
        #     worker.update()

    def place(self, pos, num):

        if self.current_state == 'worker':
            self.place_worker(pos, num)
            return

        if self.current_state == 'office':
            self.place_office(pos, num)
            return

    def place_worker(self, pos, num):
        w = Worker(pos=pos, id=len(self.workers) + 1)
        # self.workers.append(w)

        x, y = pos
        n = num

        if n >= (self.game_field.h - 1) * self.game_field.w:
            return

        cur_cell = self.game_field.data[n]
        if cur_cell['contains_office']:
            self.money -= 100
            cur_cell['canvas'].add(w.update_rectangle())

    def place_office(self, pos, num):
        x, y = pos
        n = num

        if self.is_office_being_built:
            is_placing_confirmed = False
            for i in self.office_buffer:
                if n == i:
                    is_placing_confirmed = True
                    self.money -= 1000
                    break

            k = 0
            for i in self.office_buffer:
                cur_cell = self.game_field.data[i]
                cur_cell['canvas'].remove(self.overlay_buffer[k])
                if is_placing_confirmed:
                    cur_cell['contains_office'] = True
                else:
                    cur_cell['canvas'].remove(self.office_texture_buffer[k])
                k += 1

            self.office_buffer.clear()
            self.office_texture_buffer.clear()
            self.overlay_buffer.clear()
            self.is_office_being_built = False
            if is_placing_confirmed:
                return

        texture = Image(source='office.png').texture
        texture.mag_filter = 'nearest'

        if n >= (self.game_field.h - 1) * self.game_field.w:
            return

        can_be_placed = (self.game_field.h - 2) * self.game_field.w <= n < (self.game_field.h - 1) * self.game_field.w
        for i in range(6):
            if self.game_field.data[n + self.game_field.w + i]['contains_office']:
                can_be_placed = True
        for i in range(6):
            if self.game_field.data[n + i]['contains_office']:
                can_be_placed = False

        k = 0
        for i in self.office_buffer:
            self.game_field.data[i]['canvas'].remove(self.overlay_buffer[k])
            k += 1
        self.office_buffer.clear()
        self.overlay_buffer.clear()

        for i in range(6):
            texture_region = texture.get_region(16 * i, 0, 16, 16)
            office_block = Rectangle(texture=texture_region,
                                     size=(100, 100),
                                     pos=(x + i * self.game_field.cell_size, y))
            cur_cell = self.game_field.data[n + i]
            if can_be_placed:
                cur_cell['canvas'].add(office_block)

                overlay = CorporationUtils.rectangle_from_image(filename='blue_overlay.png',
                                                                size=(100, 100),
                                                                pos=(x + i * self.game_field.cell_size, y))
                cur_cell['canvas'].add(overlay)

                self.office_texture_buffer.append(office_block)
                self.office_buffer.append(n + i)
                self.overlay_buffer.append(overlay)
                self.is_office_being_built = True
            else:
                overlay = CorporationUtils.rectangle_from_image(filename='red_overlay.png',
                                                                size=(100, 100),
                                                                pos=(x + i * self.game_field.cell_size, y))

                cur_cell['canvas'].add(overlay)

                self.office_buffer.append(n + i)
                self.overlay_buffer.append(overlay)


def get_game():
    return CorporationApp.get_running_app().game


def switch_state(instance):
    state = get_game().current_state
    print(state)

    if instance.text == state:
        get_game().set_state('none')
        return

    get_game().set_state(instance.text)

class CorporationApp(App):
    game = None

    def build(self):
        self.game = CorporationGame()
        self.load_gui()
        Clock.schedule_interval(self.game.tick, 1.0 / 60.0)


        return self.game

    def load_gui(self):
        build_office = Button(text='office',size_hint=(.2, .2), pos_hint={'x': .01, 'y': .79})
        build_worker = Button(text='worker',size_hint=(.2, .2), pos_hint={'x': .22, 'y': .79})
        money_display = Button(text=str(get_game().money),size_hint=(.2, .2), pos_hint={'x': .79, 'y': .79})

        get_game().money_display = money_display

        build_worker.bind(on_press=switch_state)
        build_office.bind(on_press=switch_state)

        gui = get_game().gui
        gui.add_widget(build_office)
        gui.add_widget(build_worker)
        gui.add_widget(money_display)


if __name__ == '__main__':
    CorporationApp().run()
