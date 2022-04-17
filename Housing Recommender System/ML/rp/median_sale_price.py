import numpy as np


def punishment_soft(user_value: float, data_value: float) -> float:
    return np.sqrt(user_value**(1.5) - data_value**(1.5))


def punishment_hard(user_value: float, data_value: float) -> float:
    # Formula is like this since  I want hard punishment to be negative
    # most of the time. user_value < data_value
    return np.sqrt(user_value**2 - data_value**2)


def reward_and_punishment(user_value: float, data_value: float) -> float:
    # hard punishment for data values above user value
    if user_value < data_value:
        return punishment_hard(user_value=user_value, data_value=data_value)
    # soft punishment for data values below user value
    else:
        return punishment_soft(user_value=user_value, data_value=data_value)
