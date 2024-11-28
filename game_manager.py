import pygame


class GameManager:
    def __init__(self, bg_img, screen, player, enemiesOBJ):
        self.bg_img = bg_img
        self.screen = screen
        self.player = player
        self.enemiesOBJ = enemiesOBJ
        self.bg_img_obj = pygame.image.load(self.bg_img)
        self.bg_img_obj = pygame.transform.scale(self.bg_img_obj, (1280, 720))
        self.drawItems()

    def drawItems(self):
        self.screen.blit(self.bg_img_obj, (0, 0))
        self.drawPlayer()
        self.drawEnemies()
        self.enemiesOBJ.draw_explosions(self.screen)

    def drawPlayer(self):
        self.player.draw(self.screen, self.enemiesOBJ)

    def drawEnemies(self):
        self.enemiesOBJ.draw_enemy_spaceships(self.screen)

    def init_game(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            dt = clock.tick(60) 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                self.player.move_right(self.screen)
            if keys[pygame.K_a]:
                self.player.move_left()
            if (
                keys[pygame.K_SPACE]
                and (pygame.time.get_ticks() - self.player.last_attack_time) > 200
            ):
                self.player.attack()
                self.player.last_attack_time = pygame.time.get_ticks()

            self.enemiesOBJ.update(dt)
            self.enemiesOBJ.update_explosions()
            self.drawItems()
            pygame.display.update()
