from dataclasses import dataclass

@dataclass
class PopulateConfigPeak:
    mean: int
    diff: int
    weight: int

@dataclass
class PopulateConfig:
    age_peaks: list[PopulateConfigPeak]

def getSchema():
    schemaPopulation = {
        "definitions": {
            "age_peak": {
                "properties": {
                    "mean" : {"type" : "number"},
                    "diff" : {"type" : "number"},
                    "weight" : {"type" : "number"},
                    "weight_m" : {"type" : "number"},
                    "weight_f" : {"type" : "number"}
                },
                "required": [ "mean", "diff", "weight", "weight_m", "weight_f" ],
            }
        },
        "type" : "object",
        "required": [ "age_peaks" ],
        "properties" : {
            "age_peaks" : {
                "type" : "array",
                "items": { "$ref": "#/definitions/age_peak" }
            },
        },
    }

    return schemaPopulation;

