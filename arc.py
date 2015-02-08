import pygame

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode([WIDTH, HEIGHT])
f = lambda x: HEIGHT*x*x/(WIDTH*WIDTH)
num_points = 15
arc_points = [(x, f(x)) for x in range(0, WIDTH, WIDTH//num_points)]
print(arc_points)

#draw along horizontal axis
fixed_y = 0
for p1 in arc_points:
    for p2 in arc_points:
        color = pygame.Color('white')
        if p1[0] != p2[0]:
            pygame.draw.line(screen, color, (p1[0], fixed_y), p2)

pygame.display.flip()

running = True
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = False

