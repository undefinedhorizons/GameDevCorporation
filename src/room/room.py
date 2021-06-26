from abc import ABC, abstractmethod, ABCMeta
from src.metaclass import MyMeta


class Room(ABC, metaclass=MyMeta):
    def __init__(self):
        self.price
        self.pertime
        self.capacity
        self.reliability
        self.max_reliability
        self.breakdown
        self.income

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def repair(self, amount):
        pass
