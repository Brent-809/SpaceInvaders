import pygame
import threading
from explosion import Explosion
import sprite


class Enemies(sprite.Sprite):
    def __init__(self, health, damage):
        super().__init__(0, 0, 0, 0, 0, None, None)
        self.health = health
        self.damage = damage
        self.enemies = []
        self.enemy_image = self.load_enemy_image()
        self.explosions = []

    def load_enemy_image(self):
        enemy = pygame.image.load("./assets/imgs/Enemy.png")
        enemy = pygame.transform.rotate(enemy, 180)
        enemy = pygame.transform.scale(enemy, (86, 151))
        return enemy

    def draw_enemy_spaceships(self, screen):
        if not self.enemies:

            def spawn_enemies(self):
                rows = 3
                cols = 8
                x_offset = 50
                y_offset = 50
                spacing_x = 150
                spacing_y = 150

                for row in range(rows):
                    for col in range(cols):
                        x = x_offset + col * spacing_x
                        y = y_offset + row * spacing_y
                        self.enemies.append((self.enemy_image, x, y))

            spawn_enemies(self)
        for enemy in self.enemies:
            screen.blit(enemy[0], (enemy[1], enemy[2]))

    def destroy_enemy(self, screen, enemy):
        explosion = Explosion(
            x=enemy[1],
            y=enemy[2],
        )
        self.explosions.append(explosion)
        self.enemies.remove(enemy)
        self.health -= 1

    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def draw_explosions(self, screen):
        for explosion in self.explosions:
            explosion.draw(screen)
