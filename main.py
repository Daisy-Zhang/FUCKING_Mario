import pygame
import constant
from pygame.locals import *
from sys import exit

 
pygame.init()
level = 1
screen = pygame.display.set_mode((640, 480), 0, 32)

pygame.mixer.init()                     # BGM player
pygame.mixer.music.load('BG.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()

player_image_file = 'image/player.png'
player = pygame.image.load(player_image_file).convert()
player_x = 0
player_y = 300

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
light_blue = (128, 128, 255)


inf = 1000000		#  setting the bottom limit
deadline = 700		# the falling deadline

total_jump_time = 600	# total time of a jump on a ground
height = 600	# height of a jump on a ground

move_speed = 0.8    #horizontal move speed
a = -4 * height / (total_jump_time ** 2)  # coefficient of jump action
up_speed = 0	# the speed of up going
jump_direction = 0	# 0 jump vertically    1 jump towards left    2 jump towards right

pipe = 0     # to indicate whether there is a pipe


def getGround(player_x):   # to get the ground y coordinate, it is set in advance
	if player_x <= constant.level1_back1_no_ground_start or player_x + constant.player_x_size / 2 >= constant.level1_back1_no_ground_end:
		return constant.level1_back1_ground
	elif player_x < 640:
		return inf

def toNextLevel(player_x, player_y):
    if level == 1:
        if player_x + constant.player_x_size >= 630 :
            return True
        else:
            return False


while True:

    if toNextLevel(player_x, player_y) :
        if level == 1:
            player_x = 0
            player_y = 300
            level += 1

    ground = getGround(player_x)    # the ground position y coordinate
    key_pressed = pygame.key.get_pressed()	# to get the list of whether or not a key is pressed

    if not (up_speed == 0 and player_y == ground):   # determine whether to move under gravity
    	# move under gravity
        player_y -= up_speed  # height change of each time
        up_speed += a  # speed change due to gravity

    # fall to the ground
    if player_y >= ground and player_y - ground < 10:
        player_y = ground
        up_speed = 0
        jump_direction = 0

    if (key_pressed[pygame.K_LEFT] and player_y == ground) or jump_direction == 1:
    	player_x -= move_speed  #keep moving left

    if (key_pressed[pygame.K_RIGHT] and player_y == ground) or jump_direction == 2:
    	player_x += move_speed

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and player_y == ground:
                up_speed = 1.5 		#trigger jump action at line 40
            if key_pressed[pygame.K_LEFT] and player_y == ground:
                    jump_direction = 1
            elif key_pressed[pygame.K_RIGHT] and player_y == ground:
                	jump_direction = 2
            elif event.key == K_DOWN and pipe == 1:   # for the pipe or something like that
                player_y += 30

    if player_y > deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()
    
    if player_x < 0:    #  restrict the player of going back
        player_x = 0

    if level == 1 :            
        screen.fill(light_blue)
        board_col = white
        pygame.draw.line(screen, board_col, constant.level1_board1_start, constant.level1_board1_end, 3)
        pygame.draw.line(screen, board_col, constant.level1_board2_start, constant.level1_board2_end, 3)

        pygame.draw.line(screen, board_col, constant.level1_board3_start, constant.level1_board3_end, 3)
        pygame.draw.line(screen, board_col, constant.level1_board4_start, constant.level1_board4_end, 3)
        screen.blit(player, (player_x, player_y))   

    elif level == 2 :
        screen.fill(light_blue)
        screen.blit(player, (player_x, player_y))
        board_col = white
        pygame.draw.line(screen, board_col, constant.level2_board1_start, constant.level2_board1_end, 3)
    
    pygame.display.update()

