def closest_value_in_array(value: float, array: list[float]) -> float:
    distances = [abs(x - value) for x in array]
    closest_value_index = distances.index(min(distances))
    closest_value = array[closest_value_index]
    return closest_value


def pad(string: str, width: int) -> str:
    return string + " " * (width - len(string))
