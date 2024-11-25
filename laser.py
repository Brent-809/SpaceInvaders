import pygame
import sprite

class Laser(sprite.Sprite):

    def move(self):
        self.y -= self.speed

    def draw_laser(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, enemy):
        laser_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        enemy_rect = pygame.Rect(
            enemy[1], enemy[2], enemy[0].get_width(), enemy[0].get_height())
        return laser_rect.colliderect(enemy_rect)
