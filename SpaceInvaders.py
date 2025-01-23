import pygame
import game_manager
import player
import enemies
from pygame import mixer
import serial

pygame.init()
mixer.init()

port = 'COM3'
ArduinoSerial = serial.Serial(port, 9600)

data = str(ArduinoSerial.readline().decode('ascii'))
(x, y, z) = data.split(":")
(JoyStickX, JoyStickY) = (int(x), int(y))

screen_width = 1280
screen_height = 720

enemiesOBJ = enemies.Enemies()
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

bg_music = mixer.music.load("./assets/sounds/background.wav")

game_manager = game_manager.GameManager(
    "./assets/imgs/stars.jpg", screen, playerOBJ, enemiesOBJ, bg_music, ArduinoSerial
)
game_manager.init_game()
