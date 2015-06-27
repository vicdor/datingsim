import pygame, pygame.display, pygame.mixer
import datingsim

def start():
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 80)
    text = 'Dating Sim 3000'

    fg = 0, 0, 0
    bg = 10, 140, 40
    size = font.size(text)
    ren = font.render(text, 0, fg, bg)
    screen.blit(ren, [10, 10])

    text = "Press SPACE to continue"
    alpha_iter = list(range(255, 0,-1))+list(range(0, 255))
    alpha_index = 0
    width, height = font.size(text)
    rend = font.render(text, False, [255, 255, 255])
    screen.blit(rend, [100, datingsim.WIDTH/2-width/2])

    def draw_instruct():
        nonlocal alpha_index
        alpha_index = (alpha_index + 3) % len(alpha_iter)
        rend.set_alpha(alpha_iter[alpha_index])
        screen.blit(rend, [200, datingsim.WIDTH/2-width/2])

    pygame.display.flip()

    pygame.mixer.music.load('assets/forest.wav')
    pygame.mixer.music.play()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP):
                done = True

        screen.fill(bg)
        screen.blit(ren, [10, 10])
        draw_instruct()
        pygame.display.flip()
        pygame.time.wait(1000//20)

    pygame.mixer.music.stop()
