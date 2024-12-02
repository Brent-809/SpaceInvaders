import pygame
import laser
import sprite
import explosion
import time


class Player(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image, screen, attacking=False, last_attack_time=0):
        super().__init__(x, y, width, height, speed, image, screen)
        self.lasers = []
        self.score = 0
        self.attacking = attacking
        self.last_attack_time = last_attack_time
        self.dt = 0
        self.explosions = []
        self.lives = 3
        self.invincible = False
        self.invincibility_time = 2
        self.last_hit_time = 0
        self.is_destroyed = False

    def move_left(self):
        if self.x >= 10:
            self.x -= self.speed

    def move_right(self, screen):
        right = screen.get_width()
        if self.x <= right - self.width - 10:
            self.x += self.speed

    def attack(self):
        laserIMG = pygame.image.load("./assets/imgs/Shot.png")
        laserOBJ = laser.Laser(
            x=self.x + self.width // 2,
            y=self.y,
            width=10,
            height=30,
            speed=20,
            image=laserIMG,
            screen=self.screen,
            isEnemyLaser=False,
        )
        self.lasers.append(laserOBJ)

    def game_over(self):
        self.destroy_player()
        self.is_destroyed = True

    def update_explosions(self):
        for explosion in self.explosions:
            explosion.update()
            if not explosion.is_alive:
                self.explosions.remove(explosion)

    def draw_explosions(self, screen):
        for explosion in self.explosions:
            explosion.draw(screen)

    def destroy_player(self):
        explosionOBJ = explosion.Explosion(x=self.x, y=self.y)
        self.explosions.append(explosionOBJ)

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.last_hit_time = time.time()
            if self.lives <= 0:
                self.game_over()
            else:
                small_explosion = explosion.Explosion(
                    x=self.x + self.width // 2, y=self.y + self.height // 2, width=50, height=50)
                self.explosions.append(small_explosion)

    def update_invincibility(self):
        if self.invincible and time.time() - self.last_hit_time > self.invincibility_time:
            self.invincible = False

    def is_alive(self):
        return self.lives > 0 and not self.is_destroyed

    def draw(self, screen: pygame.Surface, enemies, dt):
        self.update_invincibility()

        if not self.invincible or (self.invincible and time.time() % 0.2 < 0.1):
            aspect_ratio = self.image.get_height() / self.image.get_width()
            new_height = int(self.width * aspect_ratio)
            image = pygame.transform.scale(
                self.image, (self.width, new_height))
            screen.blit(image, (self.x, self.y - (new_height - self.height)))

        for laserOBJ in self.lasers:
            laserOBJ.draw_laser(screen)
            laserOBJ.move(dt)
            for enemy in enemies.enemies:
                if laserOBJ.check_collision(enemy):
                    enemies.destroy_enemy(enemy)
                    if laserOBJ in self.lasers:
                        self.lasers.remove(laserOBJ)
                    self.score += 10
                    break
            if laserOBJ.y < 0:
                if laserOBJ in self.lasers:
                    self.lasers.remove(laserOBJ)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        lives_text = font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        
        wave_value = enemies.wave
        wave_text = font.render(f"Wave: {wave_value}", True, (255, 255, 255))
        screen.blit(wave_text, (10, 100))
        
        self.update_explosions()
        self.draw_explosions(screen)
