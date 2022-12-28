import numpy as np
import pygame
from .constants import *


# Class responsible for the fiancee
# Starts at position (0, 0)
class Fiancee:
    def __init__(self, topleft):
        self.x = 0
        self.y = 0

        self.images = self.load_images()
        self.reset_image()

        self.init_topleft = topleft
        self.rect = self.image.get_rect(topleft=(self.init_topleft))

    @staticmethod
    def load_images():
        sprites = pygame.image.load('fiance_escape/media/fiancee.png')

        images = []
        for j in range(4):
            for i in range(3):
                img = pygame.transform.scale(sprites.subsurface((i*48, j*64), (48, 64)), block_size)
                images.append(img)

        return images

    def move(self, move):
        if (move == 'u'):
            self.y -= 1
        elif (move == 'd'):
            self.y += 1
        elif (move == 'r'):
            self.x += 1
        elif (move == 'l'):
            self.x -= 1

    def update_image(self, index):
        self.index = index
        self.image = self.images[self.index]

    def reset_image(self):
        self.update_image(4)

    def reset(self):
        self.x = 0
        self.y = 0

        self.reset_image()
        self.rect.topleft = self.init_topleft

    @property
    def xy(self):
        return self.x, self.y