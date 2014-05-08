import pygame
__author__ = 'Jeroen'

class FoundState:

    def __init__(self, image_path):
        self.image_path = image_path

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.image_path + "\\TeerbalMode\\Beep sounds\\beep.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

