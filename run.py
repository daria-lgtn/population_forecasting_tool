from argparse import ArgumentParser

from src.helpers.data import populationTotal
from src.helpers.log import log
from src.helpers.simulate import simulate
from src.helpers.visualize import visualize
from src.modules.birth.birth import ModuleBirth
from src.modules.death.death import ModuleDeath
from src.modules.module import AModule
from src.modules.populate.populate import ModulePopulate

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--population", type=int, default = 10_000_00)
    parser.add_argument("-m", "--max_age", type=int, default = 100)
    parser.add_argument("-e", "--epoch_count", type=int, default = 40)
    args = parser.parse_args()

    modules: list[AModule] = [
        ModulePopulate(),
        ModuleBirth(),
        ModuleDeath()
    ]

    population_stack = simulate(
        modules,
        args.population,
        args.max_age,
        args.epoch_count
    )

    first = populationTotal(population_stack[0])
    last = populationTotal(population_stack[-1])
    overall = list(map(lambda x: populationTotal(x), population_stack))

    log(overall, "total")

    visualize([first], save="0")
    visualize([last], save=f'{len(population_stack)}')
    visualize([first, last], simultaneous=True, save=f'0,{len(population_stack)}')
    visualize(overall, simultaneous=True, save=f'0-{len(population_stack)}')
