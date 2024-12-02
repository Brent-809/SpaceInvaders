import pygame
import sprite

class Laser(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image, screen, isEnemyLaser):
        super().__init__(x, y, width, height, speed, image, screen)
        self.isEnemyLaser = isEnemyLaser

    def move(self, dt):
        if self.isEnemyLaser:
            self.y += self.speed * dt * 0.1
        else:
            self.y -= self.speed * dt * 0.1

    def draw_laser(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, enemy):
        if not self.isEnemyLaser:
            laser_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            enemy_rect = pygame.Rect(enemy[1], enemy[2], enemy[0].get_width(), enemy[0].get_height())
            return laser_rect.colliderect(enemy_rect)
        if self.isEnemyLaser:
            laser_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            player_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            return laser_rect.colliderect(player_rect)

