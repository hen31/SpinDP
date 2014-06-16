import pygame
import os
__author__ = 'Jeroen'

class FoundState:

    def __init__(self):
        #self.image_path = image_path
        pass

    #methode die een geluids bestand afspeelt
    @staticmethod
    def play_sound():
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__) + "/Beep sounds",'beep.wav'))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue