import pygame
import box
import enemy
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

move_speed = 0      # horizental move speed
top_move_speed = 0.6    # horizontal top move speed
or_acceleration = 0.00003    # original horizental move acceleration
acceleration = or_acceleration    # horizental move acceleration
a = -4 * height / (total_jump_time ** 2)  # coefficient of jump action
up_speed = 0	# the speed of up going
jump_direction = 0	# 0 jump vertically    1 jump towards left    2 jump towards right
restrictParameter = 1

pipe = 0     # to indicate whether there is a pipe


def getGround(player_x, player_y, level):   # to get the ground y coordinate
    ground = inf
    left = 0
    right = 1
    for groundline in box.levelGround[level - 1]:
        if groundline[0] <= player_x + box.player_x_size and groundline[1] >= player_x and player_y + box.player_y_size <= groundline[2] + 2 * restrictParameter and ground > groundline[2]:
            ground = groundline[2]
            left = groundline[0]
            right = groundline[1]
    return ground, left, right

def toNextLevel(player_x, player_y):
    if player_x + box.player_x_size >= 670 :
        return True
    else:
        return False

def showMap(level):
    screen.fill(light_blue)
    box_col = white
    for box_ in box.boxes[level - 1]:
        x = box_[0][0][0]
        y = box_[1][0][0]
        length = box_[0][0][1] - box_[0][0][0]
        height = box_[1][0][1] - box_[1][0][0]
        box_col = box_[2]
        pygame.draw.rect(screen, box_col, (x, y, length, height))

    # load enemy test
    enemy1 = pygame.image.load(enemy.level1_enemy1.getEnemyImageFile()).convert()
    if enemy.level1_enemy1.judgeDeath() == enemy.constant.ENEMY_ALIVE :
        enemy.level1_enemy1.enemyMove()
        screen.blit(enemy1, (enemy.level1_enemy1.getEnemyX(), enemy.level1_enemy1.getEnemyY()))
    screen.blit(player, (player_x, player_y))   


while True:

    if toNextLevel(player_x, player_y):
        player_x = 0
        level += 1

    ground, left, right = getGround(player_x, player_y, level)    # the ground position y coordinate
    key_pressed = pygame.key.get_pressed()	# to get the list of whether or not a key is pressed

    if not (up_speed == 0 and player_y == ground):   # determine whether to move under gravity
    	# move under gravity
        player_y -= up_speed  # height change of each time
        up_speed += a  # speed change due to gravity

    # fall to the ground
    if player_y + box.player_y_size >= ground and player_y - ground < restrictParameter:
        player_y = ground - box.player_y_size
        up_speed = 0
        jump_direction = 0

    # prevent the player from crossing the aboving ground
    # reflection
    for groundline in box.levelGround[level - 1]:
        if groundline[0] <= player_x + box.player_x_size and groundline[1] >= player_x and player_y < groundline[2] and groundline[2] - player_y < 10:
            player_y = groundline[2]
            up_speed = -up_speed
            break;

    # prevent player from crossing walls
    for wallline in box.levelWall[level - 1]:
        if wallline[0] < player_y + box.player_y_size and wallline[1] > player_y:
            if wallline[2] > player_x + box.player_x_size and wallline[2] - player_x - box.player_x_size < restrictParameter:
                player_x = wallline[2] - box.player_x_size - restrictParameter
                break;
            if wallline[2] < player_x and player_x - wallline[2] < restrictParameter:
                player_x = wallline[2] + restrictParameter
                break;
            

    if (key_pressed[pygame.K_LEFT] and player_y + box.player_y_size == ground) or jump_direction == 1:
        player_x -= move_speed  #keep moving left
        player_image_file = 'image/player_re.png'
        if move_speed < top_move_speed:
            move_speed += acceleration
            acceleration += or_acceleration

    elif (key_pressed[pygame.K_RIGHT] and player_y + box.player_y_size == ground) or jump_direction == 2:
        player_x += move_speed
        player_image_file = 'image/player.png'
        if move_speed < top_move_speed:
            move_speed += acceleration
            acceleration += or_acceleration
    else:
        move_speed = 0
        acceleration = or_acceleration

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and player_y + box.player_y_size == ground:
                up_speed = 1.5 		#trigger jump action at line 40
            if key_pressed[pygame.K_LEFT] and player_y + box.player_y_size == ground:
                    jump_direction = 1
            elif key_pressed[pygame.K_RIGHT] and (player_y + box.player_y_size == ground or (player_y + box.player_y_size < left and left - player_y + box.player_y_size < 1 and player_x + box.player_x_size < left and left - player_x - box.player_y_size < 1)):
                	jump_direction = 2
            if event.key == K_DOWN and pipe == 1:   # for the pipe or something like that
                player_y += 30
    if player_y + box.player_y_size <= ground and ground - player_y - box.player_y_size < 10 and player_x + box.player_x_size < left and left - player_x - box.player_y_size < 10:
        jump_direction = 1
    if player_y + box.player_y_size <= ground and ground - player_y - box.player_y_size < 10 and player_x > right and right - player_x < 10:
        jump_direction = 2

    if player_y > deadline:   # determine whether player is falling to death
    	print('Game Over')
    	exit()
    
    if player_x < 0:    #  restrict the player of going back
        player_x = 0

    player = pygame.image.load(player_image_file).convert()
    showMap(level)

    pygame.display.update()

