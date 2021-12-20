import pygame
import mg_ui
from geometry import Point

FPS = 60
WIDTH = 1000
HEIGHT = 800
w = mg_ui.ViewWindows(10, 10, WIDTH - 20, HEIGHT / 2)


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MicroGeogebra")
    clock = pygame.time.Clock()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEWHEEL:
                w.scale(e.y)
            if pygame.mouse.get_pressed()[0] == 1:
                pos = pygame.mouse.get_pos()
                if w.in_Widget(pos):
                    w.a_shift(pos)
            else:
                w.a_shift()
        screen.fill((0, 0, 0))
        # world.draw(screen)
        # trainers_g.draw(screen)
        # battle.draw(screen)
        w.draw(screen)
        # mg_ui.draw_rounded_rect(screen, pygame.Rect((0, 0, 30, 30)), pygame.Color(50, 150, 50), 9)
        pygame.display.flip()
        clock.tick(FPS)
        # world.update()
        # battle.update()
        # trainers_g.update()
        w.update()
    pygame.quit()


if __name__ == '__main__':
    main()
