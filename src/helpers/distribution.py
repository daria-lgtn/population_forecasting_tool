def distributionCorrection(data: list[int], should_be: int):
    total = sum(data)
    left_behind = should_be - total
    placed = 0

    probabilities = [val / total for val in data]
    for index, probability in enumerate(probabilities):
        addition = round(probability * left_behind)
        data[index] += addition
        placed += addition

    return data;
    

