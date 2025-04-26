import numpy as np


def closest_value_in_array(value: float, array: list[float]) -> float:
    closest_value_index = abs(np.array(array) - value).argmin()
    closest_value = array[closest_value_index]
    return closest_value
