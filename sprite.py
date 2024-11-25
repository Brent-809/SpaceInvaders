import pygame


class Sprite(object):
    x = 0
    y = 0
    width = 0
    height = 0
    speed = 0
    image = None
    screen = None

    def __init__(self, x, y, width, height, speed, image, screen):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.image = image
        self.screen = screen
        if image is not None:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.x, self.y))