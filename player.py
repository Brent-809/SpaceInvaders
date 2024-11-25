import pygame
import laser
import sprite


class Player(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image, screen, attacking=False, last_attack_time=0):
        super().__init__(x, y, width, height, speed, image, screen)
        self.lasers = []
        self.score = 0
        self.attacking = attacking
        self.last_attack_time = last_attack_time
        

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
        )
        self.lasers.append(laserOBJ)

    def draw(self, screen: pygame.Surface, enemies):
        aspect_ratio = self.image.get_height() / self.image.get_width()
        new_height = int(self.width * aspect_ratio)
        image = pygame.transform.scale(self.image, (self.width, new_height))
        screen.blit(image, (self.x, self.y - (new_height - self.height)))

        for laserOBJ in self.lasers:
            laserOBJ.draw_laser(screen)
            laserOBJ.move()
            for enemy in enemies.enemies:
                if laserOBJ.check_collision(enemy):
                    enemies.destroy_enemy(screen, enemy)
                    self.lasers.remove(laserOBJ)
                    self.score += 10
                    break
            if laserOBJ.y < 0:
                self.lasers.remove(laserOBJ)

        # Display the score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
