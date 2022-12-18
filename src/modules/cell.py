from typing import NamedTuple

class CellData(NamedTuple):
    m: int
    f: int
    age: int

    @property
    def total(self):
        return self.m + self.f

    def add(self, another: "CellData"):
        return CellData(
            self.m + another.m,
            self.f + another.f,
            self.age
        )

    @staticmethod
    def empty(age: int):
        return CellData(0, 0, age)

    @staticmethod
    def empty_list(max: int):
        return [CellData.empty(i)
                for (i, _) in enumerate(max * [0])]


class CellChange(NamedTuple):
    inc: CellData
    dec: CellData
    label: str

    def add(self, another: "CellChange"):
        return CellChange(
            self.inc.add(another.inc),
            self.dec.add(another.dec),
            self.label + ", " + another.label
        )

    @staticmethod
    def empty(age: int, label: str):
        return CellChange(
            CellData.empty(age),
            CellData.empty(age),
            label,
        )
