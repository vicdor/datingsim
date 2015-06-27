import pygame
import time
pygame.init()

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
gameDisplay.fill((255, 255, 255))
dragging = False
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					gameDisplay.fill((255, 255, 255))
		if event.type == pygame.MOUSEBUTTONDOWN:
			start = pygame.mouse.get_pos()
			dragging = True
		if dragging:
			if event.type == pygame.MOUSEBUTTONUP:
				end = pygame.mouse.get_pos()
				pygame.draw.rect(gameDisplay, (0, 0, 0), (start[0], start[1], end[0] - start[0], end[1]- start[1]))
				#Location, color, top left x, y, width, height
				print((start[0], start[1]), end[0] - start[0], end[1]- start[1])
				dragging = False
	pygame.display.update()
	clock.tick(25)