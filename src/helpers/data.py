from ..modules.module import AModule, ModuleApply, ModuleInit
from typing import Callable, NamedTuple, Optional, TypeVar

T = TypeVar("T")
def moduleForEach(data: list[AModule], fn: Callable[[AModule], T]) -> list[T]:
    result = len(data) * [None]
    for index, entry in enumerate(data):
        result[index] = fn(entry)

    return result


def combineInit(population_list: list[ModuleInit]):
    first = population_list[0]
    rest = population_list[1:]

    for second in rest:
        first = [x.add(y) for x, y in zip(first, second)]

    return first


def combineApply(application_list: list[ModuleApply]):
    first = application_list[0]
    rest = application_list[1:]

    for second in rest:
        first = first.add(second)

    return first

def populationSum(data: list[ModuleInit]):
    return sum(map(lambda x: x.total, data))

def populationTotal(data: list[ModuleInit]):
    return list(map(lambda x: x.total, data))

def populationChange(old: list[ModuleInit], new: list[ModuleInit]):
    return round(1 - populationSum(old) / populationSum(new), 4)
