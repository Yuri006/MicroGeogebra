import math
import random
import pygame

EPS = 0.0000007


def bisector_f(a, b, c):
    p1, p2 = Circle(a, 1).cross(Line(a, b))[0], Circle(a, 1).cross(Line(a, c))[0]
    # print(Circle(p1, p1.dist(p2)).cross(Circle(p2, p1.dist(p2)))[0])
    return Line(a, Circle(p1, p1.dist(p2)).cross(Circle(p2, p1.dist(p2)))[0])


class Point:
    def __init__(self, x, y=None, polar=False):
        if type(x).__name__ == 'str':
            self.x, self.y = list(map(float, x.split()))
        elif type(x).__name__ == 'Point':
            self.x = x.x
            self.y = x.y
        elif type(x).__name__ == 'tuple':
            self.x, self.y = x
        else:
            self.x = x
            self.y = y
        if polar:
            self.x = x * math.cos(y)
            self.y = x * math.sin(y)
        self.xy = (self.x, self.y)
        self.rect = pygame.Rect(self.xy[0] - 5, self.xy[1] - 5, 10, 10)

    def get_angle(self):
        return self.to_polar()

    def update_rect(self):
        self.rect = pygame.Rect(self.x - 3, self.y - 3, self.x + 3, self.y + 3)

    def to_polar(self):
        if self.x == self.y == 0:
            return 0
        if self.y >= 0:
            return math.acos(self.x / self.dist())
        return 2 * math.pi - math.acos(self.x / self.dist())

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __abs__(self):
        return self.dist()

    def dist(self, *args):
        if not args:
            return math.hypot(self.x, self.y)
        elif len(args) == 1:
            return math.hypot(self.x - args[0].x, self.y - args[0].y)
        elif len(args) == 2:
            return math.hypot(self.x - args[0], self.y - args[1])

    def __lt__(self, other):
        return self.dist() < other.dist()

    def __le__(self, other):
        return not (self.__eq__(other) or self.__lt__(other))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.dist() > self.dist()

    def __ge__(self, other):
        return not (self.__gt__(other) or self.__eq__(other))


class Vector(Point):
    def __init__(self, *args) -> 'Vector':
        if len(args) == 1:
            super().__init__(args[0])
        if len(args) == 2:
            if type(args[0]).__name__ == ('Point' or 'Vector'):
                super().__init__(args[1].x - args[0].x, args[1].y - args[0].y)
            else:
                super().__init__(args[0], args[1])
        if len(args) == 4:
            super().__init__(args[2] - args[0], args[3] - args[1])

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def __mul__(self, other):
        return self.dot_product(other)

    def cross_product(self, other):
        return self.x * other.y - self.y * other.x

    def __xor__(self, other):
        return self.cross_product(other)

    def mul(self, n):
        return Vector(self.x * n, self.y * n)

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y)


class Line:
    def __init__(self, *args) -> 'Line':
        if len(args) == 2:
            if (type(args[0]).__name__ and type(args[1]).__name__) == 'Point':
                self.A = args[1].y - args[0].y
                self.B = args[0].x - args[1].x
                self.C = args[1].x * args[0].y - args[0].x * args[1].y
            elif type(args[0]).__name__ == 'Point' and type(args[1]).__name__ == 'Vector':
                line = Line(args[0], Point(args[0].x + args[1].x, args[0].y + args[1].y))
                self.A = line.A
                self.B = line.B
                self.C = line.C
        elif len(args) == 1:
            self.A, self.B, self.C = list(map(float, args[0].split()))
        elif len(args) == 3:
            self.A, self.B, self.C = args
        self.v = Vector(self.A, -self.B)

    def __str__(self):
        return str(self.A) + ' ' + str(self.B) + ' ' + str(self.C)

    def contains(self, p: 'Point') -> 'bool':
        if self.A * p.x + self.B * p.y + self.C == 0:
            return True
        return False

    @property
    def normal(self):
        return Vector(self.A, self.B)

    def same_side(self, p1: 'Point', p2: 'Point') -> 'bool':
        if (self.A * p1.x + self.B * p1.y + self.C) * (self.A * p2.x + self.B * p2.y + self.C) >= 0:
            return True
        return False

    def __eq__(self, other):
        if self.A * other.B == self.B * other.A and self.A * other.C == self.C * other.A and self.C * other.B == self.B * other.C:
            return True
        return False

    def is_parallel(self, other: 'Line') -> 'bool':
        if self.v ^ other.v == 0:
            return True
        return False

    def is_perpendicular(self, other: 'Line') -> 'bool':
        if self.v * other.v == 0:
            return True
        return False

    def dist(self, p: 'Point') -> 'float':
        return abs((self.A * p.x + self.B * p.y + self.C) / abs(self.normal))

    def cross(self, other: 'Line') -> 'list':
        return [Point((self.B * other.C - other.B * self.C) / (other.B * self.A - self.B * other.A),
                      (other.A * self.C - self.A * other.C) / (other.B * self.A - self.B * other.A))]

    def foot_of_perp(self, p: 'Point') -> 'Point':
        normal = self.normal
        v = Vector(self.dist(p) * normal.x / normal.dist(), self.dist(p) * normal.y / normal.dist())
        p1, p2 = Point(p.x - v.x, p.y - v.y), Point(p.x + v.x, p.y + v.y)
        # k = (self.C + self.A * p.x + self.B * self.v.x) / (self.A * self.v.x + self.B * self.v.y)
        # return Point(p.x - k * self.v.x, p.y - k * self.v.y)
        if abs(self.dist(p1)) < 1e-9:
            return p1
        return p2

    def parallel(self, d):
        k = d / abs(self.normal)
        return Line(self.A, self.B, self.C + k * (self.A * self.normal.x + self.B * self.normal.y))

    def rotate(self, angle):
        self.A, self.B = self.A * math.cos(angle) - self.B * math.sin(angle), self.B * math.cos(
            angle) + self.A * math.sin(angle)


class Circle:
    def __init__(self, *args):
        if len(args) == 1:
            self.x, self.y, self.r = list(map(int, args[0].split()))
        elif len(args) == 3:
            self.x, self.y, self.r = args[0], args[1], args[2]
        elif len(args) == 2:
            self.x, self.y, self.r = args[0].x, args[0].y, args[1]
        self.c = Point(self.x, self.y)

    def dist(self, line: 'Line') -> 'float':
        return line.dist(self.c) - self.r

    def cross(self, other: 'Line or Circle') -> 'list':
        if type(other).__name__ == 'Line':
            p = other.foot_of_perp(self.c)
            if self.dist(other) > 0:
                return []
            elif self.dist(other) == 0:
                return [p]
            else:
                d = (self.r ** 2 - (self.r + self.dist(other)) ** 2) ** 0.5
                p1, p2 = Line(self.c, other.normal).parallel(d).cross(other)[0], Line(self.c, other.normal).parallel(
                    -d).cross(other)[0]
                return [p1, p2]
        elif type(other).__name__ == 'Circle':
            if (self.c == other.c) and (self.r == other.r):
                return [0, 0, 0]
            elif self.r + other.r < self.c.dist(other.c) or self.c == other.c:
                return []
            elif (self.c.dist(other.cross(Line(self.c, other.c))[0]) > self.r and self.c.dist(
                    other.cross(Line(self.c, other.c))[1]) > self.r) or (
                    other.c.dist(self.cross(Line(self.c, other.c))[0]) > other.r and other.c.dist(
                self.cross(Line(self.c, other.c))[1]) > other.r):
                return []
            else:
                return self.cross(Line(-2 * (self.x - other.x), -2 * (self.y - other.y),
                                       self.x ** 2 + self.y ** 2 + other.r ** 2 - other.x ** 2 - other.y ** 2 - self.r ** 2))

    def see(self, p: 'Point') -> 'float':
        return (math.asin(self.r / (self.c.dist(p)))) * 2

    def touch(self, p: 'Point') -> 'list':
        p_m = Point(p.x - self.x, p.y - self.y)
        if p_m.dist() < self.r:
            return []
        elif p_m.dist() == self.r:
            return [p]
        else:
            a = math.acos(self.r / p_m.dist())
            x1 = self.r * math.sin(a - p_m.get_angle()) + self.x
            x2 = self.r * math.sin(a + p_m.get_angle()) + self.x
            y1 = self.r * math.cos(a - p_m.get_angle()) + self.y
            y2 = self.r * math.cos(a + p_m.get_angle()) + self.y
        return [Point(x1, y1), Point(x2, y2)]


class Triangle:
    def __init__(self, *args):
        if len(args) == 1:
            self.a, self.b, self.c = args[0]
        elif len(args) == 3:
            self.a, self.b, self.c = args[0], args[1], args[2]

    def bisector(self, n):
        if n == 1:
            return bisector_f(self.a, self.b, self.c)
        elif n == 2:
            return bisector_f(self.b, self.a, self.c)
        else:
            return bisector_f(self.c, self.a, self.b)

    @property
    def intersec_p_m(self):
        return Point((self.a.x + self.b.x + self.c.x) / 3, (self.a.y + self.b.y + self.c.y) / 3)

    @property
    def intersec_p_h(self):
        return Line(self.a, Line(self.b, self.c).normal).cross(Line(self.c, Line(self.a, self.b).normal))[0]

    @property
    def intersec_p_b(self):
        return self.bisector(1).cross(self.bisector(2))[0]

    @property
    def intersec_p_ch(self):
        return Line(Line(self.a, self.intersec_p_m).cross(Line(self.b, self.c))[0], Line(self.b, self.c).normal).cross(
            Line(Line(self.b, self.intersec_p_m).cross(Line(self.a, self.c))[0], Line(self.a, self.c).normal))[0]

    @property
    def described_circle(self):
        return Circle(self.intersec_p_ch, self.intersec_p_ch.dist(self.a))

    @property
    def inscribed_circle(self):
        return Circle(self.intersec_p_b, Line(self.a, self.b).dist(self.intersec_p_b))
