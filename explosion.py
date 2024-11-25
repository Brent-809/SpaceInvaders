import pygame
from sprite import Sprite

class Explosion(Sprite):
    def __init__(self, x, y, width=150, height=150):
        super().__init__(x, y, width, height, 0, None, None)
        self.images = [pygame.transform.scale(pygame.image.load(f"./assets/imgs/explosion/explosion{i}.png"), (width, height)) for i in range(1, 7)]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = (x, y)
        self.current_image = 0
        self.animation_speed = 5 
        self.counter = 0
        self.is_alive = True

    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.is_alive = False

    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.images[self.current_image], self.rect)

