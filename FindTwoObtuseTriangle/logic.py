import numpy as np
import math

#проверка на вырожденность
def is_non_degenerate_triangle(p1, p2, p3):
    return (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) != 0
def calculate_angle(side1, side2, side3):
    numerator = side1**2 + side2**2 - side3**2
    denominator = 2 * side1 * side2
    if denominator == 0:
        return 90 
    elif -1 <= numerator / denominator <= 1:
        cos_angle = numerator / denominator
        angle_radians = math.acos(cos_angle)

        # Переводим радианы в градусы
        angle_degrees = math.degrees(angle_radians)
        return angle_degrees
    else:
        return 90 

#расчет расстояния между точками
def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

#проверка на тупоугольность 
def is_obtuse_triangle(point1, point2, point3):
    side1 = calculate_distance(point1, point2)
    side2 = calculate_distance(point2, point3)
    side3 = calculate_distance(point3, point1)

    angle1 = calculate_angle(side1, side2, side3)
    angle2 = calculate_angle(side2, side3, side1)
    angle3 = calculate_angle(side3, side1, side2)

    if angle1 > 90.00001  or angle2 > 90.00001 or angle3 > 90.00001:
        return True
    else:
        return False

#формирование массива тупоугольных треугольников
def find_non_degenerate_triangles(points):
    n = len(points)
    result_triangles = []

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p1, p2, p3 = points[i], points[j], points[k]
                if is_non_degenerate_triangle(p1, p2, p3) & is_obtuse_triangle(p1,p2,p3):
                    result_triangles.append([p1, p2, p3])
    return result_triangles

#получение тупого угла
def get_obtuse_angle(triangle):
    side_lengths = [
        np.linalg.norm(np.array(triangle[1]) - np.array(triangle[0])),
        np.linalg.norm(np.array(triangle[2]) - np.array(triangle[1])),
        np.linalg.norm(np.array(triangle[0]) - np.array(triangle[2]))
    ]
    max_size = max(side_lengths)
    for i in range(3):
        if max_size == side_lengths[i]:
            max_size_index = i
    if max_size_index == 0:
        return triangle[2]
    if max_size_index == 1:
        return triangle[0]
    else:
        return triangle[1]

#посчет угла между осью абсцисс
def calculate_angle_between_line_and_x_axis(point1, point2):
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]

    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees

#функция обработки всех точек
def points_processing(points1, points2):
    triangles1 = find_non_degenerate_triangles(points1)
    triangles2 = find_non_degenerate_triangles(points2)
    max_angle = 0
    max_first = triangles1[0]
    max_second = triangles2[0]
    for first in triangles1:
        for second in triangles2:
            first_obtuse_angle = get_obtuse_angle(first)
            second_obtuse_angle = get_obtuse_angle(second)
            cur_angle = max(calculate_angle_between_line_and_x_axis(first_obtuse_angle, second_obtuse_angle), calculate_angle_between_line_and_x_axis(second_obtuse_angle, first_obtuse_angle))
            if cur_angle >= max_angle:
                max_angle = cur_angle
                max_first = first
                max_second = second
    return max_first, max_second, get_obtuse_angle(max_first), get_obtuse_angle(max_second), max_angle

