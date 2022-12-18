import os
import json
import inspect
from typing import Any
from jsonschema import validate

def readJson(schema: dict[str, Any]):
    path = os.path.dirname(inspect.stack()[1].filename)

    with open(f'{path}/config.json') as f:
        data = json.load(f)
        validate(instance=data, schema=schema)
        return data
