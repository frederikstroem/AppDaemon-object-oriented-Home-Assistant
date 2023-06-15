HOME_NAME = "Home"
MOTD = f"We bid you welcome to the {HOME_NAME}!"

def decimal_to_255(decimal_value):
    return int(round(decimal_value * 255))

def angle_to_255(action_angle):
    # One full rotation is 255.
    return int(round(action_angle * 255 / 360))
