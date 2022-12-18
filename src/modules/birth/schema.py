from dataclasses import dataclass

@dataclass
class BirthConfigPeak:
    mean: int
    diff: int
    weight: int

@dataclass
class BirthConfig:
    birth_rate_average: float
    birth_rate_female: float
    birth_rate_male: float
    birth_peaks: list[BirthConfigPeak]

def getSchema():
    schemaBirth = {
        "definitions": {
            "birth_peak": {
                "properties": {
                    "mean" : {"type" : "number"},
                    "diff" : {"type" : "number"},
                    "weight" : {"type" : "number"}
                },
                "required": [ "mean", "diff", "weight" ],
            }
        },
        "type" : "object",
        "properties" : {
            "birth_rate_average" : {"type" : "number"},
            "birth_rate_female" : {"type" : "number"},
            "birth_rate_male" : {"type" : "number"},
            "birth_peaks" : {
                "type" : "array",
                "items": { "$ref": "#/definitions/birth_peak" }
            },
        },
        "required": [ 
            "birth_peaks",
            "birth_rate_average",
            "birth_rate_female",
            "birth_rate_male"
        ],
    }

    return schemaBirth;

