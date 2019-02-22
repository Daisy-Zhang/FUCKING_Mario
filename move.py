import role
import box
import constant
import pygame
from pygame.locals import *
from sys import exit

inf = 1000000		#  setting the bottom limit


def getGround(role_x, role_y, role_x_size, role_y_size, level):   # to get the ground y coordinate
    ground = inf
    left = 0
    right = 1
    for groundline in box.levelGround[level - 1]:
        if groundline[0] <= role_x + role_x_size and groundline[1] >= role_x and role_y + role_y_size <= groundline[2] + 2 * constant.RESTRICT_PARAMETER and ground > groundline[2]:
            ground = groundline[2]
            left = groundline[0]
            right = groundline[1]
    return ground, left, right


def move(r, level):   #  r is a role object

    key_pressed = pygame.key.get_pressed()	# to get the list of whether or not a key is pressed

    ground, left, right = getGround(r.getRoleX(), r.getRoleY(), r.getRoleXSize(), r.getRoleYSize(), level)

    if not (r.getUpSpeed() == 0 and r.getRoleY() == ground):   # determine whether to move under gravity
            # move under gravity
            r.setRoleY(r.getRoleY() - r.getUpSpeed())  # height change of each time
            r.setUpSpeed(r.getUpSpeed() + r.getA())  # speed change due to gravity

    # fall to the ground
    if r.getRoleY() + r.getRoleYSize() >= ground and r.getRoleY() - ground < constant.RESTRICT_PARAMETER:
        r.setRoleY(ground - r.getRoleYSize())     #step on the ground
        r.setUpSpeed(0)       #  up speed zero
        r.setJumpDirection(0)     #  no jump

    # prevent the player from crossing the aboving ground
    # reflection
    for groundline in box.levelGround[level - 1]:
        if groundline[0] <= r.getRoleX() + r.getRoleXSize() and groundline[1] >= r.getRoleX() and r.getRoleY() < groundline[2] and groundline[2] - r.getRoleY() < 10:
            r.setRoleY(groundline[2])
            r.setUpSpeed(-r.getUpSpeed())
            break

    # prevent player from crossing walls
    for wallline in box.levelWall[level - 1]:
        if wallline[0] < r.getRoleY() + r.getRoleYSize() and wallline[1] > r.getRoleY():
            if wallline[2] > r.getRoleX() + r.getRoleXSize() and wallline[2] - r.getRoleX() - r.getRoleXSize() < constant.RESTRICT_PARAMETER:
                r.setRoleX(wallline[2] - r.getRoleXSize() - constant.RESTRICT_PARAMETER)
                break
            if wallline[2] < r.getRoleX() and r.getRoleX() - wallline[2] < constant.RESTRICT_PARAMETER:
                r.setRoleX(wallline[2] + constant.RESTRICT_PARAMETER)
                break
            

    if (key_pressed[pygame.K_LEFT] and r.getRoleY() + r.getRoleYSize() == ground) or r.getJumpDirection() == 1:
        r.setRoleX(r.getRoleX() - r.getMoveSpeed())  #keep moving left
        r.setImageFile('image/player_re.png')
        if r.getMoveSpeed() < r.getTopMoveSpeed() and not r.getJumpDirection() == 1:
            r.setMoveSpeed(r.getMoveSpeed() + r.getAcceleration())
            r.setAcceleration(r.getAcceleration() + r.getOrAcceleration())

    elif (key_pressed[pygame.K_RIGHT] and r.getRoleY() + r.getRoleYSize() == ground) or r.getJumpDirection() == 2:
        r.setRoleX(r.getRoleX() + r.getMoveSpeed())
        r.setImageFile('image/player.png')
        if r.getMoveSpeed() < r.getTopMoveSpeed() and not r.getJumpDirection() == 2:
            r.setMoveSpeed(r.getMoveSpeed() + r.getAcceleration())
            r.setAcceleration(r.getAcceleration() + r.getOrAcceleration())
    else:
        r.setMoveSpeed(0.1)
        r.setMoveSpeed(r.getOrAcceleration())

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP and r.getRoleY() + r.getRoleYSize() == ground:
                r.setUpSpeed(r.getJumpSpeed())		#trigger jump action at line 40
                if key_pressed[pygame.K_LEFT] and r.getRoleY() + r.getRoleYSize() == ground:
                    r.setJumpDirection(1)
                elif key_pressed[pygame.K_RIGHT] and r.getRoleY() + r.getRoleYSize() == ground:
                    r.setJumpDirection(2)

            if event.key == K_DOWN:   # for the pipe or something like that
                r.setRoleY(r.getRoleY() - 30)
        if r.getRoleY() + r.getRoleYSize() <= ground and ground - r.getRoleY() - r.getRoleYSize() < 10 and r.getRoleX() + r.getRoleXSize() < left and left - r.getRoleX() - r.getRoleXSize() < 10:
	        r.setJumpDirection(1)
        if r.getRoleY() + r.getRoleYSize() <= ground and ground - r.getRoleY() - r.getRoleYSize() < 10 and r.getRoleX() > right and right - r.getRoleX() < 10:
	        r.setJumpDirection(2)

    if r.getRoleX() < 0:    #  restrict the player of going back
        r.setRoleX(0)
