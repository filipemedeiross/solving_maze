import numpy as np
import pygame
from .constants import *


# Class responsible for the fiancee
# Starts at position (0, 0)
class Fiancee:
    def __init__(self, topleft):
        self.__x = 0
        self.__y = 0

        self.images = []

        sprite_sheet = pygame.image.load('fiance_escape/media/fiancee.png')
        for j in range(4):
            for i in range(3):
                img = pygame.transform.scale(sprite_sheet.subsurface((i*48, j*64), (48, 64)),
                                            (block_size, block_size))
                self.images.append(img)
        
        self.index = 4
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(topleft))

    def init_pos(self, place):
        self.__x = 0
        self.__y = 0

        self.rect.topleft = place

    def move(self, move):
        if (move == 'u'):
            self.__y -= 1
        elif (move == 'd'):
            self.__y += 1
        elif (move == 'r'):
            self.__x += 1
        elif (move == 'l'):
            self.__x -= 1

    def update_image(self, index):
        self.index = index
        self.image = self.images[self.index]

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def xy(self):
        return self.x, self.y
