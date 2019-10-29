from point import point
import math


def calculate_mid_distance(point_1: point, point_2: point):
    point_1_mid = point_1.get_mid_point()
    point_2_mid = point_2.get_mid_point()
    return math.sqrt(math.pow(point_1_mid[0] - point_2_mid[0], 2) + math.pow(point_1_mid[1] - point_2_mid[1], 2))


def calculate_margin(point: point):
    mid_point = point.get_mid_point()
    edge_point = point.get_top_left()
    return math.sqrt(math.pow(mid_point[0] - edge_point[0], 2) + math.pow(mid_point[1] - edge_point[1], 2))


def calc_outer_product(a, b, p):
    return (p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])


def calc_relative_distance(obstacle: point, person: point):
    d1 = calc_outer_product(obstacle.get_mid_point(), obstacle.get_bottom_right(), person.get_mid_point())
    d2 = calc_outer_product(obstacle.get_mid_point(), obstacle.get_top_right(), person.get_mid_point())
    c = calculate_mid_distance(obstacle, person)
    if d1 > 0:
        if d2 > 0:
            a = obstacle.y_1 - person.y_2
            b = obstacle.get_mid_point()[1] - person.get_mid_point()[1] + 1
            return "TOP", a * c / b
        else:
            a = person.x_1 - obstacle.x_2
            b = person.get_mid_point()[0] - obstacle.get_mid_point()[0] + 1
            return "RIGHT", a * c / b
    else:
        if d2 > 0:
            a = obstacle.x_1 - person.x_2
            b = obstacle.get_mid_point()[0] - person.get_mid_point()[0] + 1
            return "LEFT", a * c / b
        else:
            a = person.y_1 - obstacle.y_2
            b = person.get_mid_point()[1] - obstacle.get_mid_point()[1] + 1
            return "BOTTOM", a * c / b

# obstacle = point(1, 1)
# obstacle.set_x_coordinates(8, 11)
# obstacle.set_y_coordinates(9, 13)
#
# person1 = point(1, 1)
# person2 = point(1, 1)
# person3 = point(1, 1)
# person4 = point(1, 1)
#
# person1.set_x_coordinates(14, 16)
# person1.set_y_coordinates(8, 10)
# person2.set_x_coordinates(11, 13)
# person2.set_y_coordinates(4, 6)
# person3.set_x_coordinates(3, 5)
# person3.set_y_coordinates(6, 8)
# person4.set_x_coordinates(10, 12)
# person4.set_y_coordinates(16, 18)
#
# print(calc_relative_distance(obstacle, person1))
# print(calc_relative_distance(obstacle, person2))
# print(calc_relative_distance(obstacle, person3))
# print(calc_relative_distance(obstacle, person4))
