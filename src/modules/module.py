from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ..helpers.visualize import visualize
from .cell import CellChange, CellData

ModuleSeed = None
ModuleInit = list[CellData]
ModuleValidate = list[any]
ModuleApply = CellChange

class AModule:
    __metaclass__ = ABCMeta
    label: str

    def __init__(self, label: str):
        self.label = label

    @abstractmethod
    #   считывание json конфигурации и формирование внутренних распределений
    def seed(self, population: int, max_age: int) -> ModuleSeed:
        raise NotImplementedError

    @abstractmethod
    #   генерация базового распределения
    def init(self, max_age: int) -> ModuleInit:
        return CellData.empty_list(max_age)

    @abstractmethod
    #   применение модуля и изменение популяции на конкретном возрасте
    def apply(self, entry: CellData) -> ModuleApply:
        return CellChange.empty(entry.age, self.label)

    @abstractmethod
    #   метод валидации работы модуля
    def validate(self, input: ModuleInit) -> ModuleValidate:
        raise NotImplementedError
        # if plot:
        #     visualize([result.seed, result.data], show=True, title=self.name())

