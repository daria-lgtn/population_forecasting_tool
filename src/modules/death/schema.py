from dataclasses import dataclass

@dataclass
class DeathConfigPeak:
    mean: int
    diff: int
    weight: int

@dataclass
class DeathConfig:
    death_rate_female: float
    death_rate_male: float
    death_peaks: list[DeathConfigPeak]

def getSchema():
    schemaDeath = {
        "definitions": {
            "death_peak": {
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
            "death_rate_female" : {"type" : "number"},
            "death_rate_male" : {"type" : "number"},
            "death_peaks" : {
                "type" : "array",
                "items": { "$ref": "#/definitions/death_peak" }
            },
        },
        "required": [ 
            "death_peaks",
            "death_rate_female",
            "death_rate_male"
        ],
    }

    return schemaDeath;

