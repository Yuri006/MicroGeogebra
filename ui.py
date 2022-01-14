import pygame.draw

import geometry as g
import pygame as p


def draw_point(select, points, screen):
    for i in points:
        p.draw.rect(screen, p.Color('blue'), i.rect)
    for i in range(len(points)):
        color = 'grey11'
        if i in select:
            color = 'darkred'
        p.draw.circle(screen, p.Color(color), points[i].xy, 2)


def get_id(name, all_list):
    c = 0
    for i in all_list:
        if i[0][:i[0].index('_')] == name:
            c += 1
    return c


class Viewer:
    def __init__(self, WIDTH, HEIGHT):
        self.h = HEIGHT
        self.w = WIDTH
        self.selected = []
        self.points = []
        self.figure = []
        self.text = 'Nothing'
        self.start_moving = None

    def draw(self, screen):
        self.draw_figure(screen)
        draw_point(self.selected, self.points, screen)

    def get_text(self):
        return self.text

    def set_text(self, text):
        self.text = text

    def update(self):
        pass

    def add_point(self, pos):
        self.points.append(g.Point(pos))

    def select(self, points):
        print(points)
        print(self.selected)
        for n in points:
            if n == -1:
                self.selected = []
            elif n in self.selected:
                self.selected.remove(n)
            else:
                self.selected.append(n)

    def collision_point(self, pos):
        c = []
        for i in range(len(self.points)):
            if self.points[i].rect.collidepoint(pos):
                c.append(i)
        return c

    def move_point(self, pos, start):
        if start:
            if self.start_moving is None:
                self.start_moving = pos
                new_pos = 0
                shift = (0, 0)
            else:
                new_pos = pos
                shift = (self.start_moving[0] - new_pos[0], self.start_moving[1] - new_pos[1])
                self.start_moving = new_pos
            print(self.start_moving, new_pos)
            for i in self.selected:
                self.points[i] = g.Point(self.points[i].xy[0] - shift[0],  self.points[i].xy[1] - shift[1])
        else:
            self.start_moving = None

    def remove_point(self):
        self.points = [j for i, j in enumerate(self.points) if i not in self.selected]
        self.selected = []

    def point_pos(self, n):
        return self.points[n].xy[0] - self.w / 2, -(self.points[n].xy[1] - self.h / 2)

    def str_point_pos(self, n):
        return [str(self.points[n].xy[0] - self.w / 2), str(-(self.points[n].xy[1] - self.h / 2))]

    def add_figure(self, figure):
        print(self.figure)
        if len(self.selected) >= 2:
            if figure == 'Line':
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Line' and i[1] == [self.selected[0], self.selected[1]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Line_' + str(get_id('Line', self.figure)), [self.selected[0], self.selected[1]]])
                self.text = 'Create ' + 'Line_' + str(get_id('Line', self.figure))
                return 1
            elif figure == 'Triangle' and len(self.selected) >= 3:
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Triangle' and i[1] == [self.selected[0], self.selected[1],
                                                                         self.selected[2]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Triangle_' + str(get_id('Triangle', self.figure)),
                                    [self.selected[0], self.selected[1], self.selected[2]]])
                self.text = 'Create ' + 'Triangle_' + str(get_id('Triangle', self.figure))
                return 1
            elif figure == 'Circle':
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Circle' and i[1] == [self.selected[0], self.selected[1]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(
                    ['Circle_' + str(get_id('Circle', self.figure)), [self.selected[0], self.selected[1]]])
                self.text = 'Create ' + 'Circle_' + str(get_id('Circle', self.figure))
                return 1
            '''            if figure == 'Section':
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Section' and i[1] == [self.selected[0], self.selected[1]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Section' + str(get_id('Line', self.figure)), [self.selected[0], self.selected[1]]])
                self.text = 'Create ' + 'Section_' + str(get_id('Line', self.figure))
                return 1'''

    def draw_figure(self, screen):
        for f in self.figure:
            if f[0][:f[0].index('_')] == 'Circle':
                pygame.draw.circle(screen, p.Color('green'), self.points[f[1][0]].xy, self.points[f[1][0]].dist(self.points[f[1][1]]), 2)
            elif f[0][:f[0].index('_')] == 'Triangle':
                pygame.draw.polygon(screen, p.Color('green'), [self.points[f[1][i]].xy for i in range(3)], 2)
            elif f[0][:f[0].index('_')] == 'Line':
                l_1 = g.Line(g.Point(0, 0), g.Point(self.w, 0))
                l_2 = g.Line(g.Point(0, 0), g.Point(0, self.h))
                l_3 = g.Line(g.Point(0, self.h), g.Point(self.w, self.h))
                l_4 = g.Line(g.Point(self.w, 0), g.Point(self.w, self.h))
                start_end = []
                for i in [l_1, l_2, l_3, l_4]:
                    crosser = i.cross(g.Line(g.Point(self.points[f[1][0]].xy), g.Point(self.points[f[1][1]].xy)))
                    if len(crosser) != 0:
                        start_end.append(crosser[0])
                pygame.draw.line(screen, p.Color('green'), start_end[0].xy, start_end[1].xy, 2)
            '''
            elif f[0][:f[0].index('_')] == 'Section':
                pygame.draw.aaline(screen, p.Color('green'), self.points[f[1][0]].xy, self.points[f[1][1]].xy, 2)
            '''


