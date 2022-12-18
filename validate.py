from argparse import ArgumentParser

from src.helpers.data import combineInit, moduleForEach
from src.helpers.visualize import visualize
from src.modules.birth.birth import ModuleBirth
from src.modules.death.death import ModuleDeath
from src.modules.module import AModule
from src.modules.populate.populate import ModulePopulate

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--population", type=int, default = 10_000_00)
    parser.add_argument("-m", "--max_age", type=int, default = 100)
    args = parser.parse_args()

    modules: list[AModule] = [
        ModulePopulate(),
        ModuleBirth(),
        ModuleDeath(),
    ]

    moduleForEach(modules, lambda x: x.seed(args.population, args.max_age))
    population_data = combineInit(moduleForEach(modules, lambda x: x.init(args.max_age)))
    moduleForEach(modules, lambda x: visualize(x.validate(population_data), show=True))
