import pygame
import sprite
from PIL import Image, ImageSequence

class Explosion(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image, screen: pygame.Surface):
        super().__init__(x, y, width, height, speed, image, screen)
        self.screen = screen
        self.index = 0
        self.current_time = 0
        self.animation_time = 100

        self.explosion_frames = [
            pygame.image.load(f"./assets/imgs/explosion/explosion{i}.png")
            for i in range(1, 6)
        ]
        self.explosion_frames = [
            pygame.transform.scale(frame, (150, 150)) for frame in self.explosion_frames
        ]
        self.frame_duration = 1500 // len(self.explosion_frames)
        self.last_update = pygame.time.get_ticks()
        self.current_frame = 0

    def play_animation(self):
        
        for frame in self.explosion_frames:
            self.screen.blit(frame, (self.x, self.y))
            pygame.display.flip()
            pygame.time.wait(100)
            self.update()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.explosion_frames):
                self.current_frame = 0
            self.image = self.explosion_frames[self.current_frame]
