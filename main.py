import pygame

from settings import *


class Main:
    def __init__(self):
        # init pygame and the size of the window
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')

        self.background = [pygame.Rect((col + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                           for col in range(0, COLUMNS, 2) for row in range(ROWS)]

    def draw_background(self):
        self.display_surface.fill(LIGHT_GREEN)
        for rectangle in self.background:
            pygame.draw.rect(self.display_surface, DARK_GREEN, rectangle)

    def run(self):
        running = True
        while running:
            self.display_surface.fill((0, 0, 0))
            main.draw_background()  # draws the checkered background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT
                    running = False
            pygame.display.update()


main = Main()
#main.draw_background()
main.run()
