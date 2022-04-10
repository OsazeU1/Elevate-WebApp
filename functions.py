from sympy import Point, Polygon, Circle


def create_user_polygon(lat, lng, accuracy):

    user = Circle(Point(lat, lng), accuracy)

    return user



def is_overlap(polygon1, polygon2):

    intersect = polygon1.intersection(polygon2)
    isIntersect = True if len(intersect) > 0 else False

    return [isIntersect, polygon2]


    
# TODO:
def create_building_polygon(field):

    return