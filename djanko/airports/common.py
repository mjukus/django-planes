import math

def get_distance_between(point1, point2):
    '''http://www.movable-type.co.uk/scripts/latlong.html'''
    R = 6371E3
    lat1 = point1.latitude
    long1 = point1.longitude
    lat2 = point2.latitude
    long2 = point2.longitude
    phi1 = lat1 * math.pi/180
    phi2 = lat2 * math.pi/180
    delta_phi = (lat2-lat1) * math.pi/180
    delta_lambda = (long2-long1) * math.pi/180

    a = math.sin(delta_phi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c / 1000

def within_range(location, range, airports):
    airports_within_range = []
    for airport in airports:
        distance = get_distance_between(location, airport)
        if distance < range:
            airports_within_range.append(airport)
    return airports_within_range