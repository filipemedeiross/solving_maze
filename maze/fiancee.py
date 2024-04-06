from pygame.image import load
from pygame.transform import scale
from .constants import FIANCEE_PATH, FIANCEE_I, FIANCEE_J, \
                       FIANCEE_W, FIANCEE_H, FIANCEE_INIT, \
                       BLOCK_SIZE


class Fiancee:
    def __init__(self, topleft):
        self.x = 0
        self.y = 0
        self.topleft = topleft

        self.load_images()
        self.reset_image()

    def load_images(self):
        sprites = load(FIANCEE_PATH)

        self.images = []
        for j in range(FIANCEE_J):
            for i in range(FIANCEE_I):
                image = sprites.subsurface((i*FIANCEE_W, j*FIANCEE_H),
                                           (  FIANCEE_W,   FIANCEE_H))

                self.images.append(scale(image, BLOCK_SIZE))

    def update_image(self, index, topleft):
        self.index = index
        self.image = self.images[self.index]
        self.rect  = self.image.get_rect(topleft=topleft)

    def reset_image(self):
        self.update_image(FIANCEE_INIT, self.topleft)

    def reset(self):
        self.x = 0
        self.y = 0

        self.reset_image()

    def move(self, move):
        if move == 'l':
            self.x -= 1
        elif move == 'r':
            self.x += 1
        elif move == 'u':
            self.y -= 1
        elif move == 'd':
            self.y += 1

    @property
    def xy(self):
        return self.x, self.y
