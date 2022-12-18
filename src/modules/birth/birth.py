import numpy as np
from src.helpers.distribution import distributionCorrection
from src.helpers.json import readJson
from tqdm import tqdm

from ..cell import CellChange, CellData
from ..module import (AModule, ModuleApply, ModuleInit, ModuleSeed,
                      ModuleValidate)
from .schema import BirthConfig, BirthConfigPeak, getSchema


class ModuleBirth(AModule):
    config: BirthConfig
    probabilities: list[float]

    def __init__(self):
        super().__init__("Модуль рождаемости")

    def seed(self, population: int, max_age: int) -> ModuleSeed:
        config = readJson(getSchema())
        self.config = BirthConfig(**config)
        self.probabilities = self.__seed(population, max_age)

    #   генерация базового распределения (наследуется)
    # def init(self) -> ModuleInit:

    def apply(self, entry: CellData) -> ModuleApply:
        result = round(self.probabilities[entry.age] * entry.f)

        change_f = int(result * self.config.birth_rate_female)
        change_m = int(result * self.config.birth_rate_male)

        return CellChange(
            CellData(change_m, change_f, entry.age),
            CellData.empty(entry.age),
            self.label
        )

    def validate(self, input: ModuleInit) -> ModuleValidate:
        max_age = len(input);
        population_f = sum(map(lambda x: x.f, input))
        population_m = sum(map(lambda x: x.m, input))
        population = population_f + population_m;
        
        total_birth = 0
        total_birth_f = 0
        total_birth_m = 0
        birth_list = [0] * max_age

        for age in range(0, max_age):
            applied = self.apply(CellData(0, population, age))
            birth_list[age] = applied.inc.total

            total_birth_f += applied.inc.f
            total_birth_m += applied.inc.m
            total_birth += applied.inc.total
        
        print("всего родилось (всего/мужчин/женщин):", 
            total_birth, total_birth_m, total_birth_f)
        print("рождаемость:", round(total_birth / population, 4))
        print("соотношение (м\ж):", round(total_birth_m / total_birth, 4))
        print("массив рождений:", birth_list)
        
        return [
            birth_list,
            self.probabilities
        ]

    def __seed(self, population: int, max_age: int):
        #   генерация распределения
        total_weight = sum(x["weight"] for x in self.config.birth_peaks)
        population_multiplier = population / total_weight

        #   конкатенация равномерных распределений
        def peakToNormal(peak: BirthConfigPeak):
            return np.random.normal(peak["mean"], peak["diff"], round(population_multiplier * peak["weight"]))

        distribution = np.concatenate(
            [peakToNormal(x) for x in self.config.birth_peaks])

        #   конвертация распределения в массив вероятностей рождения
        data = [0] * max_age
        print(f'>>> Модуль рождаемости. Генерация распределения')
        for age in tqdm(distribution, bar_format="{l_bar} {bar}"):
            index = round(age)
            #   будут выбросы, выходящие за пределы диапазона жизни
            if (index >= 0 and index < max_age):
                data[index] += 1

        #   коррекция распределения с учетом выбросов
        corrected = distributionCorrection(data, population)

        total = sum(corrected) / self.config.birth_rate_average
        probabilities = [val / total for val in data]
        return probabilities
