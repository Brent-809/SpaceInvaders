import pygame
import random
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
        self.spawn_timer = 0
        self.spawn_delay = 1000
        self.max_enemies = 24
        self.screen_width = 1280
        self.screen_height = 620

    def load_enemy_image(self):
        enemy = pygame.image.load("./assets/imgs/Enemy.png")
        enemy = pygame.transform.rotate(enemy, 180)
        enemy = pygame.transform.scale(enemy, (86, 151))
        return enemy

    def spawn_enemy(self):
        if len(self.enemies) < self.max_enemies:
            x = random.randint(0, self.screen_width - 86)
            y = random.randint(-200, -50)
            dx = random.uniform(-1, 1)
            dy = random.uniform(0.5, 1.5)
            self.enemies.append([self.enemy_image, x, y, dx, dy])

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_enemy()
            self.spawn_timer = 0

        for enemy in self.enemies:
            enemy[1] += enemy[3] * dt * 0.1 
            enemy[2] += enemy[4] * dt * 0.1 

            if enemy[1] <= 0 or enemy[1] >= self.screen_width - 86:
                enemy[3] *= -1
            if enemy[2] >= self.screen_height - 151:
                enemy[4] *= -1
            if 0 <= enemy[1] <= self.screen_width - 86 and 0 <= enemy[2] <= self.screen_height - 151:
                if enemy[2] <= 0:
                    enemy[4] *= -1

    def draw_enemy_spaceships(self, screen):
        for enemy in self.enemies:
            screen.blit(enemy[0], (int(enemy[1]), int(enemy[2])))

    def destroy_enemy(self, enemy):
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
