import pygame
import random
from explosion import Explosion
import sprite
import laser


class Enemies(sprite.Sprite):
    def __init__(self, health, damage):
        super().__init__(0, 0, 0, 0, 0, None, None)
        self.health = health
        self.damage = damage
        self.enemies = []
        self.enemy_image = self.load_enemy_image()
        self.explosions = []
        self.player = None
        self.screen = None
        self.spawn_timer = 0
        self.spawn_delay = 1000
        self.max_enemies = 24
        self.screen_width = 1280
        self.screen_height = 620
        self.real_screen_height = 720
        self.lasers = []
        self.shot_timers = [random.uniform(0, 1)
                            for _ in range(self.max_enemies)]
        self.shot_delay = 3000
        self.last_shot_time = 0
        self.wave = 1

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

    def spawn_wave(self, screen):
        self.screen = screen
        for _ in range(self.wave * 5):
            self.spawn_enemy()
            self.draw_wave_number()

    def draw_enemy_spaceships(self, screen, player):
        self.player = player
        for enemy in self.enemies:
            screen.blit(enemy[0], (int(enemy[1]), int(enemy[2])))

    def draw_explosions(self, screen):
        for explosion in self.explosions:
            explosion.draw(screen)

    def destroy_enemy(self, enemy):
        explosion = Explosion(x=enemy[1], y=enemy[2])
        self.explosions.append(explosion)
        self.enemies.remove(enemy)
        self.health -= 1

    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

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

            if enemy[2] <= 0:
                enemy[2] = 0
                enemy[4] *= -1
            elif enemy[2] >= self.screen_height - 151:
                enemy[4] *= -1

        player_lasers = self.player.lasers if self.player else []
        player_score = self.update_lasers(dt, player_lasers, 0)

        if not self.enemies:
            self.wave += 1
            self.spawn_wave(self.screen)

    def shoot_lasers(self, current_time):
        if current_time - self.last_shot_time >= self.shot_delay:
            shooting_enemies = random.sample(
                self.enemies, min(4, len(self.enemies)))
            for enemy in shooting_enemies:
                laserIMG = pygame.image.load("./assets/imgs/Shot.png")
                laserOBJ = laser.Laser(
                    x=enemy[1] + 43,
                    y=enemy[2] + 151,
                    width=10,
                    height=30,
                    speed=5,
                    image=laserIMG,
                    screen=None,
                    isEnemyLaser=True,
                )
                self.lasers.append(laserOBJ)
            self.last_shot_time = current_time

    def update_lasers(self, dt, player_lasers, player_score=0):
        for laserOBJ in self.lasers[:]:
            laserOBJ.move(dt)
            if laserOBJ.y > self.real_screen_height:
                self.lasers.remove(laserOBJ)
            elif self.player and laserOBJ.check_collision(self.player):
                self.player.take_damage()
                self.lasers.remove(laserOBJ)

        for laserOBJ in player_lasers[:]:
            laserOBJ.move(dt)
            for enemy in self.enemies[:]:
                if laserOBJ.check_collision(enemy):
                    self.destroy_enemy(enemy)
                    if laserOBJ in player_lasers:
                        player_lasers.remove(laserOBJ)
                    player_score += 10
                    break
            if laserOBJ.y < 0:
                if laserOBJ in player_lasers:
                    player_lasers.remove(laserOBJ)
        if self.player:
            self.player.score += player_score
        return player_score

    def draw_lasers(self, screen):
        for laserOBJ in self.lasers:
            laserOBJ.draw_laser(screen)

    def draw_wave_number(self):
        font = pygame.font.Font(None, 48)
        wave_text = font.render(
            f"Wave: {self.wave}", True, (255, 255, 255))
        if self.screen:
            self.screen.blit(wave_text, (10, 100))
            print("Wave number successfully draw")
