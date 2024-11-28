import pygame
import game_manager
import player
import enemies

pygame.init()

screen_width = 1280
screen_height = 720

enemiesOBJ = enemies.Enemies(100, 10)
screen = pygame.display.set_mode((screen_width, screen_height))
bottom = screen.get_height() - 145.5
center = screen.get_width() // 2

player_sprite = pygame.image.load("./assets/imgs/Char.png")
playerOBJ = player.Player(
    x=center,
    y=bottom,                       
    width=86.5,
    height=145.5,
    speed=10,
    image=player_sprite,
    screen=screen,
)

game_manager = game_manager.GameManager(
    "./assets/imgs/stars.jpg", screen, playerOBJ, enemiesOBJ
)
game_manager.init_game()

