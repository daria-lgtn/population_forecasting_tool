from tqdm import tqdm

from ..modules.module import AModule
from .data import combineInit, moduleForEach
from .epoch import epoch


def simulate(
        modules: list[AModule],
        population: int, 
        max_age: int, 
        epoch_count: int
    ):

    moduleForEach(modules, lambda x: x.seed(population, max_age))
    population_data = combineInit(moduleForEach(modules, lambda x: x.init(max_age)))
        
    population_stack = [population_data]

    print(f'>>> Симуляция. Число эпох: {epoch_count}')
    for _ in tqdm(range(0, epoch_count), bar_format="{l_bar} {bar}"):
        epoch_data = epoch(modules, population_data)
        population_new_data = epoch_data.data

        population_stack.append(population_new_data)
        population_data = population_new_data

    return population_stack
