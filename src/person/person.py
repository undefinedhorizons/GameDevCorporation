from src.metaclass import MyMeta
from utils import GameObject, get_game
from abc import ABC, abstractmethod
from enum import Enum


class Status(Enum):
    WORKING = 1
    RESTING = 2
    GOING_TO_WORK = 3
    TOILET = 4


class Person(ABC, metaclass=MyMeta):
    def __init__(self):
        self.price
        self.salary
        self.income
        self.status
        self.fatigue
        self.toilet
        self.office

        self.working_pos

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def move_work(self):
        pass

    @abstractmethod
    def move_rest(self):
        pass

    @abstractmethod
    def move(self, step):
        pass

    @abstractmethod
    def on_press(self):
        pass
