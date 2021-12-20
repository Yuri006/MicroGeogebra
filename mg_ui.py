import pygame.gfxdraw
import pygame as p
from geometry import *


class ViewWindows(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        self.color = pygame.Color(255, 255, 255)
        self.r = p.Rect((x, y, width, height))
        self.main_center = Point(self.r.center)
        self.center = self.main_center
        self.shift = (0, 0)
        self.sides = {'top': Line(Point(x, y), Point(x + width, y)),
                      'bottom': Line(Point(x, y + height), Point(x + width, y + height)),
                      'right': Line(Point(x, y), Point(x, y + height)),
                      'left': Line(Point(x + width, y), Point(x + width, y + height))
                      }

        self.axis = [(Line(self.center, self.sides['top'].normal).cross(self.sides['top'])[0],
                      Line(self.center, self.sides['top'].normal).cross(self.sides['bottom'])[0]),
                     (Line(self.center, self.sides['right'].normal).cross(self.sides['right'])[0],
                      Line(self.center, self.sides['right'].normal).cross(self.sides['left'])[0])]
        self.axis_line = [Line(self.axis[0][0], self.axis[0][1]), Line(self.axis[1][0], self.axis[1][1])]

        self.shift_trigger = [None, Point(self.center.x + self.shift[0], self.center.y + self.shift[1])]

        self.cells = DynamicCell(self.axis_line, self.sides, 1)

    def update(self) -> None:
        self.axis = [(Line(Point(self.center.x + self.shift[0], self.center.y + self.shift[1]),
                           self.sides['top'].normal).cross(self.sides['top'])[0],
                      Line(Point(self.center.x + self.shift[0], self.center.y + self.shift[1]),
                           self.sides['top'].normal).cross(self.sides['bottom'])[0]),
                     (Line(Point(self.center.x + self.shift[0], self.center.y + self.shift[1]),
                           self.sides['right'].normal).cross(self.sides['right'])[0],
                      Line(Point(self.center.x + self.shift[0], self.center.y + self.shift[1]),
                           self.sides['right'].normal).cross(self.sides['left'])[0])]
        self.axis_line = [Line(self.axis[0][0], self.axis[0][1]), Line(self.axis[1][0], self.axis[1][1])]
        self.cells.update(self.axis_line)

    def a_shift(self, pos=None):
        if (self.shift_trigger[0] is None) and (pos is not None):
            self.shift_trigger[0] = pos
            # click
        elif pos is None:
            self.center = self.shift_trigger[1]
            self.shift_trigger[0] = None
            self.shift = (0, 0)
            # unpressed
        else:
            self.shift = (-(self.shift_trigger[0][0] - pos[0]), -(self.shift_trigger[0][1] - pos[1]))
            self.shift_trigger[1] = Point(self.center.x + self.shift[0], self.center.y + self.shift[1])
            # pressed

    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, self.r, 0, 0)
        self.cells.draw(screen)
        pygame.draw.line(screen, p.Color('grey'), self.axis[0][0].xy, self.axis[0][1].xy, 3)
        pygame.draw.line(screen, p.Color('grey'), self.axis[1][0].xy, self.axis[1][1].xy, 3)
        pygame.draw.circle(screen, p.Color('grey'), self.shift_trigger[1].xy, 4)
        # self.cells.draw(screen)

    def in_Widget(self, pos):
        return self.r.collidepoint(pos)

    def scale(self, scale):
        self.cells.scale(scale)


class DynamicCell:
    def __init__(self, axis_line, rect_side, width=1, size=9, color=p.Color('darkslategray4')):
        self.color = color
        self.width = width
        self.axis = axis_line
        self.sides = rect_side
        self.main_center = self.axis[0].cross(self.axis[1])[0]
        self.center = self.main_center
        self.size = size
        self.main_lines = self.generate_cells()

    def update(self, new_axis):
        self.axis = new_axis
        self.center = self.axis[0].cross(self.axis[1])[0]
        self.main_lines = self.generate_cells()

    def draw(self, screen):
        drawing = [pygame.draw.line(screen, self.color, i[0].xy, i[1].xy, self.width) for i in self.main_lines]

    def generate_cells(self):
        left = round(self.sides['left'].dist(self.center) / self.size, 0)
        right = round(self.sides['right'].dist(self.center) / self.size, 0)
        top = round(self.sides['top'].dist(self.center) / self.size, 0)
        bottom = round(self.sides['bottom'].dist(self.center) / self.size, 0)
        # print(left, right, top, bottom)
        l_line = [(self.axis[0].parallel(-self.size * i).cross(self.sides['top'])[0],
                   self.axis[0].parallel(-self.size * i).cross(self.sides['bottom'])[0]) for i in range(int(left))]
        r_line = [(self.axis[0].parallel(self.size * i).cross(self.sides['top'])[0],
                   self.axis[0].parallel(self.size * i).cross(self.sides['bottom'])[0]) for i in range(int(right))]
        t_line = [(self.axis[1].parallel(self.size * i).cross(self.sides['left'])[0],
                   self.axis[1].parallel(self.size * i).cross(self.sides['right'])[0]) for i in range(int(bottom))]
        b_line = [(self.axis[1].parallel(-self.size * i).cross(self.sides['left'])[0],
                   self.axis[1].parallel(-self.size * i).cross(self.sides['right'])[0]) for i in range(int(top))]
        return l_line + r_line + t_line + b_line

    def scale(self, scale):
        self.size += 2 * scale
