import pygame
from pygame.locals import *
from sys import exit
from random import randint
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

player_image_file = 'image/player.jpeg'
 
player = pygame.image.load(player_image_file).convert()

player_x = 0
player_y = 140

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            flag_up = 0
            if event.key == K_LEFT:
                player_x -= 10
            elif event.key == K_RIGHT:
                player_x += 10
            elif event.key == K_UP:
                player_y -= 30
            elif event.key == K_DOWN:
                player_y += 30

    screen.fill((0,0,0))
    board_col = (255, 255, 255)
    pygame.draw.line(screen, board_col, (0, 350), (500, 350), 3)
    pygame.draw.line(screen, board_col, (500, 350), (500, 480), 3)
    screen.blit(player, (player_x, player_y))            
    
    pygame.display.update()

