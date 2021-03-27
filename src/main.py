from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.graphics.instructions import Canvas
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

Builder.load_string('''
<RV>:
    # size_hint: .5, .5
    # pos_hint: {'center': (.5, .5)}
    viewclass: 'Cell'

    RecycleGridLayout:
        cols: 10
        rows: 10
        default_size: 100, 100
        default_size_hint: None, None
        size_hint_y: None
        size_hint_x: None
        size: self.minimum_size
''')


class Cell(Button):
    def __init__(self, **kwargs):
        super(Button, self).__init__(**kwargs)
        if kwargs != {}:
            self.position = kwargs['position']
        self.r = None


    def on_press(self):
        print('TOUCH!', self.position)

        texture = Image(source='bedrock.png').texture
        # texture.min_filter = 'nearest'
        texture.mag_filter = 'nearest'
        self.r = Rectangle(texture=texture,
                           size=(100, 100),
                           pos=self.position)

        self.canvas.add(self.r)

    def on_release(self):
        print('RELEASE...', self.position)
        self.canvas.remove(self.r)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'canvas': Canvas(), 'position': (x % 10 * 100, 900 - x // 10 * 100)} for x in range(100)]
        for i in range(1):
            texture = Image(source='bedrock.png').texture
            # texture.min_filter = 'nearest'
            texture.mag_filter = 'nearest'
            self.data[i]['canvas'].add(Rectangle(texture=texture,
                                                 size=(100, 100),
                                                 pos=(i % 10 * 100, 900 - i // 10 * 100)))

        # for x in range(16):
        #     print(400 - x // 10 * 100, x % 10 * 100)


class TestApp(App):
    def build(self):
        a = RV()

        return a


if __name__ == '__main__':
    TestApp().run()
