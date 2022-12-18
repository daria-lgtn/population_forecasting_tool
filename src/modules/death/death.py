import math
import numpy as np
from src.helpers.distribution import distributionCorrection
from src.helpers.json import readJson
from tqdm import tqdm

from ..cell import CellChange, CellData
from ..module import (AModule, ModuleApply, ModuleInit, ModuleSeed,
                      ModuleValidate)
from .schema import DeathConfig, DeathConfigPeak, getSchema


class ModuleDeath(AModule):
    config: DeathConfig
    probabilities: list[float]

    def __init__(self):
        super().__init__("Модуль смертности")

    def seed(self, population: int, max_age: int) -> ModuleSeed:
        config = readJson(getSchema())
        self.config = DeathConfig(**config)
        self.probabilities = self.__seed(population, max_age)

    #   генерация базового распределения (наследуется)
    # def init(self) -> ModuleInit:

    def apply(self, entry: CellData) -> ModuleApply:
        result = round(self.probabilities[entry.age] * entry.total)

        change_f = int(result * self.config.death_rate_female)
        change_m = int(result * self.config.death_rate_male)

        return CellChange(
            CellData.empty(entry.age),
            CellData(change_m, change_f, entry.age),
            self.label
        )

    def validate(self, input: ModuleInit) -> ModuleValidate:
        max_age = len(input);
        population_f = sum(map(lambda x: x.f, input))
        population_m = sum(map(lambda x: x.m, input))
        population_t = population_f + population_m;
        population = population_t;

        total_died = 0
        total_died_f = 0
        total_died_m = 0
        death_list = [0] * max_age

        for age in range(0, max_age):
            applied = self.apply(CellData(0, population, age))
            death_list[age] = applied.dec.total

            total_died_f += applied.dec.f
            total_died_m += applied.dec.m
            total_died += applied.dec.total

            population = max(0, population - applied.dec.total)

        print("всего умерло (всего/мужчин/женщин):", total_died, total_died_m, total_died_f)
        print("процент от исходной популяции:", round(total_died / population_t, 4))
        print("соотношение (м\ж):", round(total_died_m / total_died, 4))
        print("массив смертей:", death_list)

        return [
            death_list,
            self.probabilities,
        ]
        
    def __seed(self, population: int, max_age: int):
        #   генерация распределения
        total_weight = sum(x["weight"] for x in self.config.death_peaks)
        population_multiplier = population / total_weight

        #   конкатенация равномерных распределений
        def peakToNormal(peak: DeathConfigPeak):
            return np.random.normal(peak["mean"], peak["diff"], round(population_multiplier * peak["weight"]))

        distribution = np.concatenate(
            [peakToNormal(x) for x in self.config.death_peaks])

        #   конвертация распределения в массив вероятностей рождения
        data = [0] * max_age
        print(f'>>> Модуль смертности. Генерация распределения')
        for age in tqdm(distribution, bar_format="{l_bar} {bar}"):
            index = round(age)
            #   будут выбросы, выходящие за пределы диапазона жизни
            if (index >= 0 and index < max_age):
                data[index] += 1

        #   коррекция распределения с учетом выбросов
        corrected = distributionCorrection(data, population)

        total = sum(corrected)
        probabilities = [(val / total) for val in data]

        weight_adapt = self.seed_adapt(population, probabilities)
        probabilities = [(val * weight_adapt) for val in probabilities]

        return probabilities

    def seed_adapt(self, population: int, probabilities: list[float]):
        weight = 1

        while True:
            left_over = population
            for p in probabilities:
                left_over -= left_over * p * weight

            weight += 0.1

            if (left_over / population < 0.01):
                return weight

        

        

