import pygame
__author__ = 'Jeroen'

class FoundState:

    def __init__(self):

        pass

    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.load("C:\\Users\\Jeroen\\Documents\\GitHub\\SpinDP\\SpinOS\\TeerbalMode\\Beep sounds\\beep.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

