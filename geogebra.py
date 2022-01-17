import pygame
import ui
import tkinter as tk
from pygame.locals import *
from functools import partial
from tkinter import messagebox

FPS = 60
WIDTH = 800
HEIGHT = 400
cell = 10


def draw_cell(screen, m):
    if m:
        for i in range(int(WIDTH / cell)):
            pygame.draw.line(screen, pygame.Color('grey'), (i * cell, 0), (i * cell, HEIGHT))
        for i in range(int(HEIGHT / cell)):
            pygame.draw.line(screen, pygame.Color('grey'), (0, i * cell), (WIDTH, i * cell))
    pygame.draw.line(screen, pygame.Color('black'), (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    pygame.draw.line(screen, pygame.Color('black'), (0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


def quit_callback():
    running = False


def main():
    viewer = ui.Viewer(WIDTH, HEIGHT)
    saver = ui.Save()

    pygame.init()
    pygame.mixer.init()
    window = tk.Tk()
    window.title('MicroGebra Panel')
    window.protocol("WM_DELETE_WINDOW", quit_callback)
    main_dialog = tk.Frame(window)

    action_text = tk.StringVar()

    action_text.set('Nothing')

    main_dialog.pack()
    label = tk.Label(
        textvariable=action_text,
        fg=viewer.get_text_color(),
        bg="black",
        height=2
    )
    label.pack(fill=tk.X)
    button = tk.Button(
        text="Line",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Line")
    )
    button.pack(padx=5, pady=10, side=tk.LEFT)
    button = tk.Button(
        text="Triangle",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Triangle")
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    button = tk.Button(
        text="Circle",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Circle")
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    button = tk.Button(
        text="Mega",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Mega-Circle")
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    button = tk.Button(
        text="Mini",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Mini-Circle")
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    button = tk.Button(
        text="Clear",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=viewer.clear_all
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    '''
    button = tk.Button(
        text="Section",
        width=10,
        height=2,
        bg="gray",
        fg="yellow",
        command=partial(viewer.add_figure, "Section")
    )
    button.pack(padx=5, pady=20, side=tk.LEFT)
    '''
    messagebox.showinfo('Tutorial', 'Use SHIFT+RMB to select point or move point')
    messagebox.showinfo('Tutorial', 'Use LRM to add point')
    messagebox.showinfo('Tutorial', 'Use Panel to add figure')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MicroGebra")
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            pressed = pygame.key.get_pressed()
            if e.type == MOUSEMOTION:
                p = viewer.original_pos(e.pos)
                viewer.set_text('X:' + str(p[0]) + ' Y:' + str(p[1]))
                viewer.set_text_color('green')
            if pressed[pygame.K_LSHIFT]:
                if e.type == MOUSEMOTION and e.buttons[0]:
                    # print(viewer.points[viewer.selected[0]].xy)
                    viewer.move_point(e.pos, 1)
                elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                    viewer.move_point(e.pos, 0)
                    select_points_n = viewer.collision_point(e.pos)
                    if len(select_points_n) != 0:
                        viewer.set_text('X:' + ' Y:'.join(viewer.str_point_pos(select_points_n[-1])))
                    viewer.select(select_points_n)
                elif e.type == MOUSEBUTTONDOWN and e.button == 3:
                    viewer.set_text('X:' + str(e.pos[0]) + ' Y:' + str(e.pos[1]))
                    viewer.add_point(e.pos)
                    viewer.select([-1])
            elif e.type == MOUSEBUTTONDOWN and e.button == 3:
                p = viewer.original_pos(e.pos)
                viewer.set_text('X:' + str(p[0]) + ' Y:' + str(p[1]))
                viewer.add_point(e.pos)
                viewer.select([-1])
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DELETE or e.key == pygame.K_BACKSPACE:
                    viewer.remove_point()
                if e.mod & pygame.KMOD_CTRL:
                    if e.key == pygame.K_z:
                        s_save = saver.last_action('select')
                        f_save = saver.last_action('figure')
                        p_save = saver.last_action('points')
                        if s_save:
                            viewer.selected = s_save
                        if f_save:
                            viewer.figure = f_save
                        if p_save:
                            viewer.points = p_save
                        print(viewer.selected)
                        print(viewer.figure)
                        print(viewer.points)
        screen.fill((255, 255, 255))
        print(viewer.figure)
        action_text.set(viewer.get_text())
        label.config(fg=viewer.get_text_color())
        main_dialog.update()
        saver.new_action('select', viewer.selected.copy())
        saver.new_action('figure', viewer.figure.copy())
        saver.new_action('points', viewer.points.copy())
        draw_cell(screen, 0)
        viewer.draw(screen)
        # w.draw(screen)
        pygame.display.flip()
        # w.update()
    main_dialog.destroy()


pygame.quit()

if __name__ == '__main__':
    main()
