def soft_punishment(user_value: float, data_value: float) -> float:
    # I want closer values to have more weight
    return 1/abs(user_value - data_value)


def hard_punishment(user_value: float, data_value: float) -> float:
    # I want closer values to have more weight
    return 1/abs(user_value - data_value)


def reward_and_punishment(user_value: float, data_value: float) -> float:
    # hard punishment for data values above user value
    if user_value < data_value:
        return hard_punishment(user_value=user_value, data_value=data_value)
    # soft punishment for data values below user value
    else:
        return soft_punishment(user_value=user_value, data_value=data_value)
