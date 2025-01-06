import pygame
import random
from explosion import Explosion
import sprite
import laser


class Enemies(sprite.Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, None, None)
        self.enemies = []
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
        self.wavemanager = None

    def load_enemy_image(self, enemy_image):
        enemy = pygame.image.load(enemy_image)
        enemy = pygame.transform.rotate(enemy, 180)
        enemy = pygame.transform.scale(enemy, (86, 151))
        return enemy

    def spawn_enemy(self, enemy_type):
        if len(self.enemies) < self.max_enemies:
            x = random.randint(0, self.screen_width - 86)
            y = random.randint(-200, -50)
            dx = random.uniform(-1, 1) * enemy_type["speed"]
            dy = random.uniform(0.5, 1.5) * enemy_type["speed"]
            image = self.load_enemy_image(enemy_type["image"])
            self.enemies.append(
                [image, x, y, dx, dy, enemy_type["health"], enemy_type["damage"]])

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

    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            enemy_type = self.wavemanager.get_enemy_type()
            self.spawn_enemy(enemy_type)
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
            self.wavemanager.update_wave()

    def set_wave_manager(self, wave_manager):
        self.wavemanager = wave_manager

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
                    damage=enemy[6]  # Use enemy's damage for the laser
                )
                self.lasers.append(laserOBJ)
            self.last_shot_time = current_time

    def update_lasers(self, dt, player_lasers, player_score=0):
        for laserOBJ in self.lasers[:]:
            laserOBJ.move(dt)
            if laserOBJ.y > self.real_screen_height:
                self.lasers.remove(laserOBJ)
            elif self.player and laserOBJ.check_collision(self.player):
                self.player.take_damage(laserOBJ.damage)
                self.lasers.remove(laserOBJ)

        for laserOBJ in player_lasers[:]:
            laserOBJ.move(dt)
            for enemy in self.enemies[:]:
                if laserOBJ.check_collision(enemy):
                    enemy[5] -= laserOBJ.damage  # Subtract laser damage from enemy health
                    if enemy[5] <= 0:
                        self.destroy_enemy(enemy)
                        player_score += 10 * self.wavemanager.wave
                    if laserOBJ in player_lasers:
                        player_lasers.remove(laserOBJ)
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
