def distance(latitude1, longitude1, latitude2, longitude2):
    from math import sin, cos, sqrt, atan2, radians

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    # approximate radius of earth in km
    r = 6373.0

    dlon = lon1 - lon2
    dlat = lat1 - lat2

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


def is_in_range(a1, a2, b1, b2, radius):
    if distance(a1, a2, b1, b2) <= radius:
        return 1
    else:
        return 0
