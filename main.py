import pygame
import constant
from pygame.locals import *
from sys import exit
 
pygame.init()
level = 1
screen = pygame.display.set_mode((640, 480), 0, 32)

player_image_file = 'image/player.png'
player = pygame.image.load(player_image_file).convert()
player_x = 0
player_y = 300

ground = 300	# the ground position y coordinate
total_jump_time = 400	# total time of a jump
height = 200	# height of a jump
jump_time = total_jump_time	# jump time

pipe = 0

while True:

    if not jump_time == total_jump_time:
        a = -4 * height / (total_jump_time ** 2)  # coefficient of jump action
        player_y -= 2 * a * jump_time - a * total_jump_time  # height elevated of each time
        jump_time += 1

        if jump_time == total_jump_time:
        	player_y = ground		# fall to the ground

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            flag_up = 0
            if event.key == K_LEFT:
                player_x -= 15
            elif event.key == K_RIGHT:
                player_x += 15
            elif event.key == K_UP and jump_time == total_jump_time:
                jump_time = 0 		#trigger jump action
            elif event.key == K_DOWN and pipe == 1:   # for the pipe or something like that
                player_y += 30

    screen.fill((0,0,0))
    board_col = (255, 255, 255)
    pygame.draw.line(screen, board_col, constant.level1_board1_start, constant.level1_board1_end, 3)
    pygame.draw.line(screen, board_col, constant.level1_board2_start, constant.level1_board2_end, 3)
    screen.blit(player, (player_x, player_y))            
    
    pygame.display.update()

