from src.cell import Cell
from utils import GameObject, get_game
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from grass import Grass
from cell import Cell


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
