import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

snake = pygame.Rect((300, 250, 30, 30))

map_width = 800
map_height = 600
line_width = 5
map_edge = pygame.Rect((0, 0, 800, 600))

move = (0,0)

run = True
while run:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen,'white', map_edge, line_width)



    pygame.draw.rect(screen, 'green', snake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                move = (-10, 0)
            if event.key == pygame.K_RIGHT:
                move = (10, 0)
            if event.key == pygame.K_UP:
                move = (0, -10)
            if event.key == pygame.K_DOWN:
                move = (0, 10)

        """if snake.colliderect(map_edge):
            print("colliding")
        else:
            print("not colloding")
"""
    pygame.display.update()

pygame.quit()