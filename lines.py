import pygame

y = 0
dir = 1
running = True
step_size = 2
repeats = 2
screen = pygame.display.set_mode((800, 600))

barcolor = []
for i in range(0, 255, step_size):
    for _ in range(repeats):
        barcolor.append((0, 0, i))
for i in range(255, 0, -step_size):
    for _ in range(repeats):
        barcolor.append((0, 0, i))
barheight = len(barcolor)

while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

    screen.fill((0, 0, 0))
    for i in range(0, barheight):
        pygame.draw.line(screen, barcolor[i], (0, y+i), (799, y+1))

    y += dir
    if y + barheight > 599 or y < 0:
        dir *= -1

    pygame.display.flip()

