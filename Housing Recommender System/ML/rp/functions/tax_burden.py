# I want to punish values above the user threshold for vaccination rate
# Reward values the lower they go above the threshold

# Linear reward
def reward(user_value: float, data_value: float) -> float:
    diff = user_value - data_value
    slope = 0.8
    constant = 2
    return (slope * diff) + constant


# Linear punish
def punishment(user_value: float, data_value: float) -> float:
    diff = user_value - data_value
    slope = 1.2
    constant = -1
    return (slope * diff) + constant


def reward_and_punishment(user_value: float, data_value: float) -> float:
    # punish tax burden above user desired value
    if user_value < data_value:
        return punishment(user_value=user_value, data_value=data_value)
    # reward tax burden below or equal desired value
    else:
        return reward(user_value=user_value, data_value=data_value)
