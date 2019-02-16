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

inf = 1000000		#  setting the bottom limit
deadline = 1000		# the falling deadline

total_jump_time = 400	# total time of a jump on a ground
height = 200	# height of a jump on a ground

move_speed = 0.5    #horizontal move speed
a = -4 * height / (total_jump_time ** 2)  # coefficient of jump action
up_speed = 0	# the speed of up going

pipe = 0     # to indicate weather there is a pipe


def getGround(player_x):   # to get the ground y coordinate, it is set in advance
	if player_x < 500:
		return 300
	elif player_x < 640:
		return inf

while True:

    ground = getGround(player_x)    # the ground position y coordinate
    key_pressed = pygame.key.get_pressed()	# to get the list of whether or not a key is pressed

    if not (up_speed == 0 and player_y == ground):   # determine whether to move under gravity
    	# move under gravity
        player_y -= up_speed  # height change of each time
        up_speed += a  # speed change due to gravity

    # fall to the ground
    if player_y >= ground:
    	player_y = ground
    	up_speed = 0

    if key_pressed[pygame.K_LEFT]:
    	player_x -= move_speed  #keep moving left

    if key_pressed[pygame.K_RIGHT]:
    	player_x += move_speed

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and player_y == ground:
                up_speed = 1.5 		#trigger jump action at line 40
            elif event.key == K_DOWN and pipe == 1:   # for the pipe or something like that
                player_y += 30

    if player_y > deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()

    screen.fill((0,0,0))
    board_col = (255, 255, 255)
    pygame.draw.line(screen, board_col, constant.level1_board1_start, constant.level1_board1_end, 3)
    pygame.draw.line(screen, board_col, constant.level1_board2_start, constant.level1_board2_end, 3)
    screen.blit(player, (player_x, player_y))            
    
    pygame.display.update()

