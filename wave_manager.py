import pygame
import random

class WaveManager:
    def __init__(self, enemiesOBJ):
        self.wave = 1
        self.enemiesOBJ = enemiesOBJ
        self.enemy_types = [
            {"image": "./assets/imgs/Enemy.png", "health": 1, "speed": 1, "damage": 1},
            {"image": "./assets/imgs/Enemy2.png", "health": 2, "speed": 1.2, "damage": 2},
            {"image": "./assets/imgs/Enemy3.png", "health": 3, "speed": 1.4, "damage": 3},
        ]

    def spawn_wave(self, screen):
        self.screen = screen
        enemy_type = self.get_enemy_type()
        for _ in range(self.wave * 5):
            self.enemiesOBJ.spawn_enemy(enemy_type)
        self.draw_wave_number()

    def get_enemy_type(self):
        if self.wave <= 3:
            return self.enemy_types[0]
        elif self.wave <= 6:
            return random.choice(self.enemy_types[:2])
        else:
            return random.choice(self.enemy_types)

    def draw_wave_number(self):
        font = pygame.font.Font(None, 48)
        wave_text = font.render(
            f"Wave: {self.wave}", True, (255, 255, 255))
        if self.screen:
            self.screen.blit(wave_text, (10, 100))
    
    def create_stronger_enemies(self):
        self.enemiesOBJ.enemy_speed += 1
        self.enemiesOBJ.enemy_health += 1
        self.enemiesOBJ.enemy_damage += 1
    
    def update_wave(self):
        self.wave += 1
        self.spawn_wave(self.screen)
