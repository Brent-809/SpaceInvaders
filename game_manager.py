import pygame
import wave_manager as waveManager
import keyboard
import threading


class GameManager:
    def __init__(self, bg_img, screen, player, enemiesOBJ, bg_music, ArduinoSerial):
        self.bg_img = bg_img
        self.screen = screen
        self.player = player
        self.enemiesOBJ = enemiesOBJ
        self.bg_img_obj = pygame.image.load(self.bg_img)
        self.bg_img_obj = pygame.transform.scale(self.bg_img_obj, (1280, 720))
        self.clock = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 74)
        self.wavemanager = None
        bg_music = bg_music
        self.arduinoSerial = ArduinoSerial
        self.play_bg_music()
        self.arduino_thread = threading.Thread(
            target=self.read_arduino_data_loop)
        self.arduino_thread.daemon = True
        self.arduino_thread.start()

    def play_bg_music(self):
        pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1)

    def drawItems(self, dt):
        self.screen.blit(self.bg_img_obj, (0, 0))
        self.drawPlayer(dt=dt)
        self.drawEnemies()
        self.enemiesOBJ.draw_explosions(self.screen)
        self.enemiesOBJ.draw_lasers(self.screen)

    def drawPlayer(self, dt):
        self.player.draw(self.screen, self.enemiesOBJ, dt=dt)

    def drawEnemies(self):
        self.enemiesOBJ.draw_enemy_spaceships(self.screen, self.player)

    def read_arduino_data(self):
        try:
            if self.arduinoSerial.in_waiting > 0:
                data = self.arduinoSerial.readline().decode('ascii').strip()
                values = data.split(":")
                if len(values) == 3:
                    x = values[0]
                    try:
                        JoyStickX = int(x)
                        joystick_speed = max(-10, min(10, JoyStickX))
                        self.player.speed = abs(joystick_speed)
                        print("X Value: ", JoyStickX, "Speed: ", self.player.speed)
                        if JoyStickX < 0:
                            print("left <-")
                            self.player.move_left()
                        elif JoyStickX > 0:
                            print("right ->")
                            self.player.move_right(self.screen)
                    except ValueError:
                        print(f"Invalid joystick value: {x}")
        except Exception as e:
            print(f"Error reading Arduino data: {e}")

    def read_arduino_data_loop(self):
        while True:
            self.read_arduino_data()

    def init_game(self):
        running = True
        clock = pygame.time.Clock()
        self.wavemanager = waveManager.WaveManager(self.enemiesOBJ)
        self.enemiesOBJ.set_wave_manager(self.wavemanager)
        self.player.set_wave_manager(self.wavemanager)
        self.wavemanager.spawn_wave(self.screen)

        while running:
            dt = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                    self.restart_game()

            if not self.game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and (pygame.time.get_ticks() - self.player.last_attack_time) > 200:
                    self.player.attack()
                    self.player.last_attack_time = pygame.time.get_ticks()

                self.enemiesOBJ.update(dt)
                self.enemiesOBJ.update_explosions()
                self.clock = dt
                self.enemiesOBJ.shoot_lasers(pygame.time.get_ticks())
                self.drawItems(dt=dt)

                if not self.player.is_alive() or self.player.is_destroyed:
                    self.game_over = True
            else:
                self.show_game_over_screen()

            self.wavemanager.update()
            pygame.display.update()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        score_text = self.font.render(
            f"Final Score: {self.player.score}", True, (255, 255, 255))
        restart_text = self.font.render(
            "Press R to Restart", True, (255, 255, 255))

        text_rect = game_over_text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2 - 50))
        score_rect = score_text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 50))
        restart_rect = restart_text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2 + 150))

        self.screen.blit(game_over_text, text_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def restart_game(self):
        self.player.lives = 3
        self.player.score = 0
        self.wavemanager.wave = 1
        self.player.x = self.screen.get_width() // 2
        self.player.y = self.screen.get_height() - 145.5
        self.player.is_destroyed = False
        self.enemiesOBJ.enemies.clear()
        self.enemiesOBJ.lasers.clear()
        self.player.lasers.clear()
        self.wavemanager.spawn_wave(self.screen)
        self.game_over = False

