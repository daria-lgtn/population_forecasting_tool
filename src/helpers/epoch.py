from dataclasses import dataclass
from ..modules.module import ModuleApply, ModuleInit, AModule
from ..modules.cell import CellData
from ..helpers.data import combineApply, moduleForEach

@dataclass
class EpochChange:
    data: list[int]
    increase: int
    decrease: int


def epoch(modules: list[AModule], data: ModuleInit):
    new_data = CellData.empty_list(len(data))
    epoch_increase = 0
    epoch_decrease = 0

    #   рассматриваем каждую возрастную группу по-отдельности
    for entry in data:
        #   применяем все модули для изменения численности популяции
        application_data = combineApply(
            moduleForEach(modules, lambda x: x.apply(entry)))

        newborn = application_data.inc
        died = application_data.dec

        epoch_increase += newborn.total
        epoch_decrease += died.total

        #   прирост населения
        new_data[0] = new_data[0].add(newborn)

        #   выжившие перемещаются в новую возрастную группу
        if (entry.age + 1 < len(data)):
            new_data[entry.age + 1] = CellData(
                entry.m - died.m,
                entry.f - died.f,
                entry.age + 1
            )
        #   за исключением предельного возраста
        else:
            epoch_decrease += died.total

    return EpochChange(data = new_data, increase = epoch_increase, decrease = epoch_decrease)
