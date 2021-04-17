from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics.instructions import Canvas
from kivy.properties import (
    ObjectProperty, BooleanProperty
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.recycleview import RecycleView


class Cell(Button):

    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        if kwargs != {}:
            self.position = kwargs['position']
            self.number = kwargs['number']
            self.contains_office = kwargs['contains_office']
        self.office_texture = None

        self.overlay = None

    def on_press(self):
        get_game().place_office(self.position, self.number)
        # self.contains_office = True
        # texture = Image(source='office.png').texture

        # buf = []
        # for i in texture.pixels:
        #     buf.append(i)
        #
        # for i in range(3, len(texture.pixels), 4):
        #     # buf[i - 3] = min(int(buf[i - 3] * 1.5), 255)
        #     buf[i - 2] = 0
        #     buf[i - 1] = 0
        #     buf[i] = 200
        #
        # arr = array('B', buf)
        #
        # texture = Texture.create(colorfmt='rgba', size=texture.size)
        # texture.blit_buffer(arr, colorfmt='rgba', bufferfmt='ubyte')
        #
        # texture.mag_filter = 'nearest'

        # self.office_texture = Rectangle(texture=texture,
        #                                 size=(600, 100),
        #                                 pos=self.position)
        # self.canvas.add(self.office_texture)


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

        # self.fill(0, 90, 'light_blue_concrete.png')
        self.fill((self.h - 1) * self.w, self.h * self.w, 'ground.png')

    def fill(self, first_pos, second_pos, filename):
        for i in range(first_pos, second_pos):
            texture = Image(source=filename).texture
            # texture.min_filter = 'nearest'
            texture.mag_filter = 'nearest'
            self.data[i]['canvas'] \
                .add(Rectangle(texture=texture,
                               size=(self.cell_size, self.cell_size),
                               pos=(i % self.w * self.cell_size,
                                    (self.h - 1) * self.cell_size - i // self.w * self.cell_size)))


class CorporationGame(BoxLayout):
    game_field = ObjectProperty(None)
    workers = []
    offices = []

    office_texture_buffer = []
    overlay_buffer = []
    office_buffer = []
    is_office_being_built = False

    current_state = 'building'

    def __init__(self, **kwargs):
        super(CorporationGame, self).__init__(**kwargs)

    def tick(self):
        pass
        # for worker in self.workers:
        #     worker.update()

    def place_office(self, pos, num):
        x, y = pos
        n = num

        if self.is_office_being_built:
            is_placing_confirmed = False
            for i in self.office_buffer:
                if n == i:
                    is_placing_confirmed = True
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

                overlay_texture = Image(source='blue_overlay.png').texture
                # texture.mag_filter = 'nearest'
                overlay = Rectangle(texture=overlay_texture,
                                    size=(100, 100),
                                    pos=(x + i * self.game_field.cell_size, y))

                cur_cell['canvas'].add(overlay)

                self.office_texture_buffer.append(office_block)
                self.office_buffer.append(n + i)
                self.overlay_buffer.append(overlay)
                self.is_office_being_built = True

                # cur_cell['contains_office'] = True
            else:
                overlay_texture = Image(source='red_overlay.png').texture
                # texture.mag_filter = 'nearest'

                overlay = Rectangle(texture=overlay_texture,
                                    size=(100, 100),
                                    pos=(x + i * self.game_field.cell_size, y))

                cur_cell['canvas'].add(overlay)

                self.office_buffer.append(n + i)
                self.overlay_buffer.append(overlay)


def get_game():
    return CorporationApp.get_running_app().game


class CorporationApp(App):
    game = None

    def build(self):
        self.game = CorporationGame()
        return self.game


if __name__ == '__main__':
    CorporationApp().run()
