from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView


Builder.load_string('''
<RV>:
    viewclass: 'Label'
    RecycleGridLayout:
        cols: 100
        rows: 100
        default_size: dp(50), dp(50)
        default_size_hint: None, None
        size_hint_y: None
        size_hint_x: None
        height: self.minimum_height
        width: self.minimum_width
''')

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(10000)]


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()