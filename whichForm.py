def get_shape_name(num_points):
    """Returns a shape name based on the number of connected points"""
    if num_points < 3:
        return "Not a valid shape"
    elif num_points == 3:
        return "Triangle"
    elif num_points == 4:
        return "Quadrilateral"
    elif num_points == 5:
        return "Pentagon"
    elif num_points == 6:
        return "Hexagon"
    elif num_points == 7:
        return "Heptagon"
    elif num_points == 8:
        return "Octagon"
    else:
        return f"{num_points}-gon"

def forme():
    return "..."