import os.path, sys
import pygame.mixer, pygame.time
mixer = pygame.mixer
time = pygame.time

main_dir = os.path.split(os.path.abspath(__file__))[0]
music_path = os.path.join(main_dir, 'assets/club.wav')

mixer.init()
sound = mixer.Sound(music_path)
channel = sound.play()

while channel.get_busy():
    pass
