import numpy as np
from src.helpers.distribution import distributionCorrection
from src.helpers.json import readJson
from src.helpers.visualize import visualize
from tqdm import tqdm

from ..cell import CellData
from ..module import AModule, ModuleInit, ModuleSeed, ModuleValidate
from .schema import PopulateConfig, PopulateConfigPeak, getSchema


class ModulePopulate(AModule):
    config: PopulateConfig

    population_m: int
    population_f: int
    probabilities_m: list[float]
    probabilities_f: list[float]

    def __init__(self):
        super().__init__("Модуль генерации населения")

    def seed(self, population: int, max_age: int) -> ModuleSeed:
        config = readJson(getSchema())
        self.config = PopulateConfig(**config)
        self.__seed(population, max_age)

    def init(self, max_age: int) -> ModuleInit:
        result_m = [round(self.probabilities_m[index] * self.population_m)
                    for index in range(0, max_age)]

        result_f = [round(self.probabilities_f[index] * self.population_f)
                    for index in range(0, max_age)]

        result = [CellData(m, f, i)
                  for (i, (m, f)) in enumerate(zip(result_m, result_f))]
        return result

    #   применение модуля и изменение популяции на конкретном возрасте (наследуется)
    # def apply(self, entry: CellData) -> ModuleApply:
    #     return ModuleApply(inc=[], dec=[])

    def validate(self, input: ModuleInit) -> ModuleValidate:
        population_f = sum(map(lambda x: x.f, input))
        population_m = sum(map(lambda x: x.m, input))
        population = population_f + population_m;
        print("всего представителей (всего/мужчин/женщин):", 
            population, population_m, population_f)

        return [
            list(map(lambda x: x.f, input)),
            self.probabilities_f,
        ]

    def __seed(self, population_total: int, max_age: int):
        key_male = "weight_m"
        key_female = "weight_f"

        male_total = sum(x[key_male] for x in self.config.age_peaks)
        female_total = sum(x[key_female] for x in self.config.age_peaks)
        weights_total = male_total + female_total

        self.population_m = int(population_total * male_total // weights_total)
        self.population_f = population_total - self.population_m

        #   генерируем отдельно распределение для мужчин и для женщин
        self.probabilities_m = self.__generate_probabilities(
            key_male, self.population_m, max_age, "m")
        self.probabilities_f = self.__generate_probabilities(
            key_female, self.population_f, max_age, "f")

    def __generate_probabilities(self, key: str, population: int, max_age: int, suffix: str):
        #   генерация распределения
        total_weight = sum(x[key] for x in self.config.age_peaks)
        population_multiplier = population / total_weight

        #   конкатенация равномерных распределений
        def peakToNormal(peak: PopulateConfigPeak):
            return np.random.normal(peak["mean"], peak["diff"], round(population_multiplier * peak[key]))

        distribution = np.concatenate(
            [peakToNormal(x) for x in self.config.age_peaks])

        #   конвертация распределения в массив вероятностей рождения
        data = [0] * max_age
        print(f'>>> Модуль популяции. Генерация распределения ({suffix})')
        for age in tqdm(distribution, bar_format="{l_bar} {bar}"):
            index = round(age)
            #   будут выбросы, выходящие за пределы диапазона жизни
            if (index >= 0 and index < max_age):
                data[index] += 1

        #   коррекция распределения с учетом выбросов
        corrected = distributionCorrection(data, population)

        total = sum(corrected)
        probabilities = [val / total for val in data]
        return probabilities
