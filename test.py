import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

snake = pygame.Rect((300, 250, 30, 30))

map_width = 800
map_height = 600
line_width = 5
map_edge = pygame.Rect((0, 0, 800, 600) )


run = True
while run:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen,'white', map_edge, line_width)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        snake.move_ip(-1, 0)
    elif key[pygame.K_w] == True:
        snake.move_ip(0, -1)
    elif key[pygame.K_d] == True:
        snake.move_ip(1, 0)
    elif key[pygame.K_s] == True:
        snake.move_ip(0, 1)

    pygame.draw.rect(screen, 'green', snake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.Rect.colliderect()


    pygame.display.update()

pygame.quit()