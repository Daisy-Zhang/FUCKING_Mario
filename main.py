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

total_jump_time = 500	# total time of a jump on a ground
height = 600	# height of a jump on a ground

move_speed = 0.6    #horizontal move speed
a = -4 * height / (total_jump_time ** 2)  # coefficient of jump action
up_speed = 0	# the speed of up going
jump_direction = 0	# 0 jump vertically    1 jump towards left    2 jump towards right
restrictParameter = 1

pipe = 0     # to indicate whether there is a pipe


def getGround(player_x, player_y, level):   # to get the ground y coordinate
    ground = inf
    for groundline in constant.levelGround[level - 1]:
        if groundline[0] <= player_x + constant.player_x_size and groundline[1] >= player_x and player_y + constant.player_y_size <= groundline[2] + 2 * restrictParameter and ground > groundline[2]:
            ground = groundline[2]
    return ground

def toNextLevel(player_x, player_y):
    if player_x + constant.player_x_size >= 670 :
        return True
    else:
        return False

def showMap(level):
    screen.fill(light_blue)
    board_col = white
    for groundline in constant.levelGround[level - 1]:
        pygame.draw.line(screen, board_col, [groundline[0], groundline[2]], [groundline[1], groundline[2]], 3)
    for wallline in constant.levelWall[level - 1]:
        pygame.draw.line(screen, board_col, [wallline[2], wallline[0]], [wallline[2], wallline[1]], 3)
    screen.blit(player, (player_x, player_y))   





while True:

    if toNextLevel(player_x, player_y):
        player_x = 0
        level += 1

    ground = getGround(player_x, player_y, level)    # the ground position y coordinate
    key_pressed = pygame.key.get_pressed()	# to get the list of whether or not a key is pressed

    if not (up_speed == 0 and player_y == ground):   # determine whether to move under gravity
    	# move under gravity
        player_y -= up_speed  # height change of each time
        up_speed += a  # speed change due to gravity

    # fall to the ground
    if player_y + constant.player_y_size >= ground and player_y - ground < restrictParameter:
        player_y = ground - constant.player_y_size
        up_speed = 0
        jump_direction = 0

    # prevent the player from crossing the aboving ground
    # reflection
    for groundline in constant.levelGround[level - 1]:
        if groundline[0] <= player_x + constant.player_x_size and groundline[1] >= player_x and player_y < groundline[2] and groundline[2] - player_y < 10:
            player_y = groundline[2]
            up_speed = -up_speed
            break;

    # prevent player from crossing walls
    for wallline in constant.levelWall[level - 1]:
        if wallline[0] < player_y + constant.player_y_size and wallline[1] > player_y:
            if wallline[2] > player_x + constant.player_x_size and wallline[2] - player_x - constant.player_x_size < restrictParameter:
                player_x = wallline[2] - constant.player_x_size - restrictParameter
                break;
            if wallline[2] < player_x and player_x - wallline[2] < restrictParameter:
                player_x = wallline[2] + restrictParameter
                break;
            

    if (key_pressed[pygame.K_LEFT] and player_y + constant.player_y_size == ground) or jump_direction == 1:
    	player_x -= move_speed  #keep moving left

    if (key_pressed[pygame.K_RIGHT] and player_y + constant.player_y_size == ground) or jump_direction == 2:
    	player_x += move_speed

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and player_y + constant.player_y_size == ground:
                up_speed = 1.5 		#trigger jump action at line 40
            if key_pressed[pygame.K_LEFT] and player_y + constant.player_y_size == ground:
                    jump_direction = 1
            elif key_pressed[pygame.K_RIGHT] and player_y + constant.player_y_size == ground:
                	jump_direction = 2
            elif event.key == K_DOWN and pipe == 1:   # for the pipe or something like that
                player_y += 30

    if player_y > deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()
    
    if player_x < 0:    #  restrict the player of going back
        player_x = 0

    showMap(level)       

    pygame.display.update()

