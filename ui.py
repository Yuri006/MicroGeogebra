import pygame.draw

import geometry as g
import pygame as p


def draw_point(select, points, screen):
    # for i in points:
    #     p.draw.rect(screen, p.Color('blue'), i.rect)
    for i in range(len(points)):
        color = 'grey11'
        if i in select:
            color = 'darkred'
        p.draw.circle(screen, p.Color(color), points[i].xy, 3)


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
        self.start_moving_pos = None
        self.text_color = 'white'

    def draw(self, screen):
        self.draw_figure(screen)
        draw_point(self.selected, self.points, screen)

    def get_text(self):
        return self.text

    def get_text_color(self):
        return self.text_color

    def set_text(self, text):
        self.text = text

    def set_text_color(self, color):
        self.text_color = color

    def update(self):
        pass

    def add_point(self, pos):
        self.set_text_color('blue')
        self.points.append(g.Point(pos))

    def select(self, points):
        self.set_text_color('white')
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
                new_pos = pos
                shift = (0, 0)
                self.start_moving_pos = pos
            else:
                new_pos = pos
                shift = (self.start_moving[0] - new_pos[0], self.start_moving[1] - new_pos[1])
                self.start_moving = new_pos
            for i in self.selected:
                self.points[i] = g.Point(self.points[i].xy[0] - shift[0], self.points[i].xy[1] - shift[1])
            p = (new_pos[0] - self.start_moving_pos[0], new_pos[1] - self.start_moving_pos[1])
            self.text = 'X:' + str(p[0]) + ' Y:' + str(-p[1])
            self.text_color = 'red'
        else:
            self.start_moving = None
            self.start_moving_pos = None

    def remove_point(self):
        to_delete = []
        for f in range(len(self.figure)):
            print(self.selected)
            print(self.figure[f][1])
            print(len(set(self.selected).intersection(set(self.figure[f][0]))))
            if len(set(self.selected).intersection(set(self.figure[f][1]))) > 0:
                to_delete.append(f)
        self.points = [j for i, j in enumerate(self.points) if i not in self.selected]
        self.selected = []
        self.figure = [j for i, j in enumerate(self.figure) if i not in to_delete]

    def point_pos(self, n):
        return self.points[n].xy[0] - self.w / 2, -(self.points[n].xy[1] - self.h / 2)

    def str_point_pos(self, n):
        return [str(self.points[n].xy[0] - self.w / 2), str(-(self.points[n].xy[1] - self.h / 2))]

    def original_pos(self, pos):
        return pos[0] - self.w / 2, -(pos[1] - self.h / 2)

    def clear_all(self):
        self.selected = []
        self.points = []
        self.figure = []

    def add_figure(self, figure):
        self.set_text_color('blue')
        if len(self.selected) >= 2:
            if figure == 'Line':
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Line' and i[1] == [self.selected[0], self.selected[1]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Line_' + str(get_id('Line', self.figure)), [self.selected[0], self.selected[1]]])
                line = g.Line(g.Point(self.points[self.selected[0]]), g.Point(self.points[self.selected[1]]))
                self.text = 'A:' + str(line.A) + ' B:' + str(line.B) + ' C:' + str(line.C)
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
            elif figure == 'Mega-Circle' and len(self.selected) >= 3:
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Mega-Circle' and i[1] == [self.selected[0], self.selected[1],
                                                                         self.selected[2]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Mega-Circle_' + str(get_id('Mega-Circle', self.figure)),
                                    [self.selected[0], self.selected[1], self.selected[2]]])
                self.text = 'Create ' + 'Mega-Circle_' + str(get_id('Mega-Circle', self.figure))
                return 1
            elif figure == 'Mini-Circle' and len(self.selected) >= 3:
                for i in self.figure:
                    if i[0][:i[0].index('_')] == 'Mini-Circle' and i[1] == [self.selected[0], self.selected[1],
                                                                         self.selected[2]]:
                        self.text = 'Copy of figure'
                        return 1
                self.figure.append(['Mini-Circle_' + str(get_id('Mini-Circle', self.figure)),
                                    [self.selected[0], self.selected[1], self.selected[2]]])
                self.text = 'Create ' + 'Mini-Circle_' + str(get_id('Mini-Circle', self.figure))
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
            if f[0][:f[0].index('_')] == 'Mega-Circle':
                t = g.Triangle([self.points[i] for i in f[1]])
                pygame.draw.circle(screen, p.Color('orange'), t.described_circle.c.xy,
                                   t.described_circle.r, 2)
            if f[0][:f[0].index('_')] == 'Mini-Circle':
                t = g.Triangle([self.points[i] for i in f[1]])
                pygame.draw.circle(screen, p.Color('brown'), t.inscribed_circle.c.xy,
                                   t.inscribed_circle.r, 2)
            elif f[0][:f[0].index('_')] == 'Circle':
                pygame.draw.circle(screen, p.Color('green'), self.points[f[1][0]].xy,
                                   self.points[f[1][0]].dist(self.points[f[1][1]]), 2)
            elif f[0][:f[0].index('_')] == 'Triangle':
                pygame.draw.polygon(screen, p.Color('blue'), [self.points[f[1][i]].xy for i in range(3)], 2)
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
                pygame.draw.line(screen, p.Color('red'), start_end[0].xy, start_end[1].xy, 2)
            '''
            elif f[0][:f[0].index('_')] == 'Section':
                pygame.draw.aaline(screen, p.Color('green'), self.points[f[1][0]].xy, self.points[f[1][1]].xy, 2)
            '''


class Save:
    def __init__(self):
        self.action_saver = {}

    def new_action(self, name, saving):
        if name not in self.action_saver:
            self.action_saver[name] = []
            self.action_saver[name].append(saving)
        else:
            # print(saving)
            # print(self.action_saver)
            if len(self.action_saver[name]) != 0 and self.action_saver[name][-1] != saving:
                # print('save')
                self.action_saver[name].append(saving)

    def last_action(self, name):
        print(self.action_saver)
        print(self.action_saver[name])
        if len(self.action_saver[name]) <= 1:
            return 0
        self.action_saver[name].pop(-1)
        return self.action_saver[name][-1]
