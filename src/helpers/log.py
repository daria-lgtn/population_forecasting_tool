from typing import Optional
import matplotlib.pyplot as plt

def log(
    input: list[list[int]], 
    save: Optional[str] = None
):
    with open(f'./result/{save}.txt', 'w') as f:
        for line in input:
            stringified = '\t,'.join(str(x) for x in line)
            f.write(f'[\t{stringified}]\n')
