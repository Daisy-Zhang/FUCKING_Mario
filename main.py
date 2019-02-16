import pygame
import time
from pygame.locals import *
from sys import exit
 
pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)

player_image_file = 'image/player.png'
 
player = pygame.image.load(player_image_file).convert()

player_x = 0
player_y = 300

jump_flag = 0

while True:
    if jump_flag == 1:
        player_y += 50
        jump_flag = 0

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            flag_up = 0
            if event.key == K_LEFT:
                player_x -= 15
            elif event.key == K_RIGHT:
                player_x += 15
            elif event.key == K_UP:
                jump_flag = 1
                player_y -= 50
            elif event.key == K_DOWN:   # for the pipe or something like that
                player_y += 30

    screen.fill((0,0,0))
    board_col = (255, 255, 255)
    pygame.draw.line(screen, board_col, (0, 350), (500, 350), 3)
    pygame.draw.line(screen, board_col, (500, 350), (500, 480), 3)
    screen.blit(player, (player_x, player_y))            
    
    pygame.display.update()

