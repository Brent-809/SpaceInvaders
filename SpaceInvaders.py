import pygame
import game_manager
import player
import enemies

pygame.init()

enemiesOBJ = enemies.Enemies(100, 10)
screen = pygame.display.set_mode((1280, 720), )
bottom = screen.get_height() - 65
center = screen.get_width() // 2

player_sprite = pygame.image.load("./assets/imgs/Char.png")
playerOBJ = player.Player(
    x=center,
    y=bottom,
    width=100,
    height=100,
    speed=10,
    image=player_sprite,
    screen=screen,
)

game_manager = game_manager.GameManager(
    "./assets/imgs/stars.jpg", screen, playerOBJ, enemiesOBJ
)
game_manager.init_game()
