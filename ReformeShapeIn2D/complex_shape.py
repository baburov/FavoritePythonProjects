from math import *
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"p{self.x, self.y}"

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def move(self, point):
        self += point

    def turn(self, center, angle):
        # Сохраняем значения до вычислений
        original_x = self.x 
        original_y = self.y

        # Вычисляем новые координаты
        self.x = center.x + (original_x - center.x) * cos(angle) - (original_y - center.y) * sin(angle)
        self.y = center.y + (original_x - center.x) * sin(angle) + (original_y - center.y) * cos(angle)

    def scale(self, center, kx, ky):
        self.x = kx * self.x + center.x * (1 - kx)
        self.y = ky * self.y + center.y * (1 - ky)

class PolygonException(Exception):
    pass


class Polygon:
    def __init__(self, points, points_count=3):
        if len(points) < points_count:
            raise PolygonException("Not enough points")
        self.points = points

    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self):
        if self.current >= len(self.points):
            raise StopIteration
        else:
            self.current += 1
            return self.points[self.current - 1]

    def __repr__(self):
        return f"Quadrilateral({', '.join(map(str, self.points))})"

    def move(self, point):
        for p in self:
            p.move(point)

    def turn(self, center, angle):
        for p in self:
            p.turn(center, angle)

    def scale(self, center, kx, ky):
        for p in self:
            p.scale(center, kx, ky)
    def draw(self, canvas):
        points = [(p.x, p.y) for p in self.points]
        canvas.create_polygon(points, fill="", outline='black')#, width=2)


class Quadrilateral(Polygon):
    def __init__(self, points):
        super().__init__(points, points_count=4)

class Arc(Polygon):
    def __init__(self, radius, offset, orientation):
        self.radius = radius
        ps = []
        for i in range(-orientation * radius + offset.x, orientation + offset.x, orientation):
            for j in range(-radius + offset.y, radius + 1 + offset.y, 1):
                if (i - offset.x) ** 2 + (j - offset.y) ** 2 == radius ** 2:
                    ps.append(Point(i, j))
        super().__init__(sorted(ps, key=lambda point: atan2(point.y - offset.y, point.x - offset.x)), len(ps))

class Circle(Polygon):
    def __init__(self, radius, offset):
        self.radius = radius
        eps = 0.01
        ps = []
        for i in range(5 * (-radius + offset.x), 5 * (radius + 1 + offset.x), 1):
            for j in range(5 * (-radius + offset.y), 5 * (radius + 1 + offset.y), 1):
                if radius ** 2 - eps <= (i/5 - offset.x) ** 2 + (j/5 - offset.y) ** 2 <= radius ** 2 + eps:
                    ps.append(Point(i/5, j/5))
        super().__init__(sorted(ps, key=lambda point: atan2(point.y - offset.y, point.x - offset.x)), len(ps))

class ComplexShape:
    def __init__(self):
        center = 400
        self.target = Polygon([Point(center - 20, center), Point(center + 20, center), Point(center, center), Point(center, center - 20), Point(center, center + 20), Point(center, center)], 6)
        self.circle = Circle(20, Point(center, center))
        self.rhombus = Quadrilateral([Point(center, center + 50), Point(center - 90, center), Point(center, center - 50), Point(center + 90, center)])
        self.rectangle = Quadrilateral([Point(center + 90, center + 50), Point(center - 90, center + 50), Point(center - 90, center - 50), Point(center + 90, center - 50)])
        self.arc1 = Arc(50, Point(center + 90, center), -1)
        self.arc2 = Arc(50, Point(center - 90, center), 1)
    def draw(self, canvas):
        canvas.delete("all")
        self.target.draw(canvas)
        self.circle.draw(canvas)
        self.rhombus.draw(canvas)
        self.rectangle.draw(canvas)
        self.arc1.draw(canvas)
        self.arc2.draw(canvas)
    def move(self, point):
        self.target.move(point)
        self.circle.move(point)
        self.rhombus.move(point)
        self.rectangle.move(point)
        self.arc1.move(point)
        self.arc2.move(point)
    def turn(self, center, angle):
        self.target.turn(center, angle)
        self.circle.turn(center, angle)
        self.rhombus.turn(center, angle)
        self.rectangle.turn(center, angle)
        self.arc1.turn(center, angle)
        self.arc2.turn(center, angle)
    def scale(self, center, kx, ky):
        self.target.scale(center, kx, ky)
        self.circle.scale(center, kx, ky)
        self.rhombus.scale(center, kx, ky)
        self.rectangle.scale(center, kx, ky)
        self.arc1.scale(center, kx, ky)
        self.arc2.scale(center, kx, ky)

# a = Arc(5, Point(0, 0), 1)
# print(a)
# a.move(Point(1, 2))
# print(a)