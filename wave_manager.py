import pygame
import random
import math

class WaveManager:
    def __init__(self, enemiesOBJ):
        self.wave = 1
        self.enemiesOBJ = enemiesOBJ
        self.enemy_types = [
            {"image": "./assets/imgs/Enemy.png", "health": 1, "speed": 1, "damage": 1},
            {"image": "./assets/imgs/Enemy2.png", "health": 2, "speed": 1.2, "damage": 2},
            {"image": "./assets/imgs/Enemy3.png", "health": 3, "speed": 1.4, "damage": 3},
        ]
        self.enemies_per_wave = 1
        self.screen = None
        self.wave_complete = False
        self.wave_transition_timer = 0
        self.wave_transition_duration = 3000  # 3 seconds

    def spawn_wave(self, screen):
        self.screen = screen
        self.wave_complete = False
        enemy_type = self.get_enemy_type()
        for _ in range(self.enemies_per_wave):
            self.enemiesOBJ.spawn_enemy(enemy_type)

    def get_enemy_type(self):
        if self.wave <= 3:
            return self.enemy_types[0]
        elif self.wave <= 6:
            return random.choice(self.enemy_types[:2])
        else:
            return random.choice(self.enemy_types)
    
    def create_stronger_enemies(self):
        for enemy_type in self.enemy_types:
            enemy_type["health"] += 1
            enemy_type["speed"] += 0.2
            enemy_type["damage"] += 1
    
    def update_wave(self):
        if len(self.enemiesOBJ.enemies) == 0 and not self.wave_complete:
            self.wave_complete = True
            self.wave_transition_timer = pygame.time.get_ticks()

        if self.wave_complete:
            current_time = pygame.time.get_ticks()
            if current_time - self.wave_transition_timer >= self.wave_transition_duration:
                self.wave += 1
                self.create_stronger_enemies()
                self.spawn_wave(self.screen)
            else:
                self.draw_wave_transition_effect()

    def draw_wave_transition_effect(self):
        if self.screen:
            font = pygame.font.Font(None, 72)
            wave_text = font.render(f"Wave {self.wave} Complete!", True, (255, 255, 255))
            text_rect = wave_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            
            alpha = int(255 * (0.5 + 0.5 * abs(math.sin(pygame.time.get_ticks() * 0.005))))
            text_surface = pygame.Surface(wave_text.get_size(), pygame.SRCALPHA)
            text_surface.fill((255, 255, 255, alpha))
            text_surface.blit(wave_text, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            self.screen.blit(text_surface, text_rect)

    def update(self):
        self.update_wave()
