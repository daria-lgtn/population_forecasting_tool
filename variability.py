from argparse import ArgumentParser

from src.helpers.data import populationSum
from src.helpers.simulate import simulate
from src.modules.birth.birth import ModuleBirth
from src.modules.death.death import ModuleDeath
from src.modules.module import AModule, ModuleInit
from src.modules.populate.populate import ModulePopulate

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--population", type=int, default = 10_000_00)
    parser.add_argument("-m", "--max_age", type=int, default = 100)
    parser.add_argument("-e", "--epoch_count", type=int, default = 50)
    parser.add_argument("-v", "--variation_count", type=int, default = 50)
    args = parser.parse_args()

    modules: list[AModule] = [
        ModulePopulate(),
        ModuleBirth(),
        ModuleDeath()
    ]

    population_variation: list[ModuleInit] = []

    for i in range(0, args.variation_count):
        print(f'>>> Симуляция {i}/{args.variation_count}')
        population_stack = simulate(
            modules,
            args.population,
            args.max_age,
            args.epoch_count
        )

        population_variation.append(population_stack[-1])

    population_variation_total = list(map(lambda x: populationSum(x), population_variation))
    population_variation_min = min(population_variation_total)
    population_variation_max = max(population_variation_total)
    population_variation_avg = round(sum(population_variation_total) / len(population_variation_total))

    print("вариативность (нижний - средний - верхний):", 
        population_variation_min, population_variation_avg, population_variation_max)
