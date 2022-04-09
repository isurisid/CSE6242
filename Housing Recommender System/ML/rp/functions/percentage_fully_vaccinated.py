# I want to heavily punish values under the user threshold for vaccination rate
# Reward values the higher they go above the threshold

# Linear reward
def reward(user_value: float, data_value: float) -> float:
    diff = data_value - user_value
    slope = 0.8
    constant = 2
    return (slope * diff) + constant


# Quadratic punish
def punishment(user_value: float, data_value: float) -> float:
    diff = data_value - user_value
    quad_coeff = 1.2
    lin_coeff = 0.8
    constant = 2
    return -1 * ((quad_coeff * (diff**2)) + (lin_coeff * diff) + constant)


# R&P function for percentage fully vaccinated
def reward_and_punishment(user_value: float, data_value: float) -> float:
    # punishment for data values below user value
    if user_value > data_value:
        return punishment(user_value=user_value, data_value=data_value)
    # reward for data values above user value
    else:
        return reward(user_value=user_value, data_value=data_value)
