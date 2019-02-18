player_x_size = 46
player_y_size = 50

green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
earth = (237, 145, 33)

num = 3   # number of levels

def box(x, y, length, height, color):   # return [boxGrounds, boxWalls]
	return [[[x, x + length, y], [x, x + length, y + height]], [[y, y + height, x], [y, y + height, x + length]], color]

boxes = []

#  level 1
boxes.append([box(0, 350, 500, 130, green), box(600, 350, 40, 130, green)])

#  level 2
boxes.append([box(0, 350, 640, 130, green)])

#  level 3
boxes.append([box(0, 350, 300, 130, green), box(150, 300, 100, 50, earth), box(300, 200, 150, 50, white), box(400, 320, 240, 160, green)])

levelGround = []
levelWall = []

for level in range(num):
    levelGround.append([])
    levelWall.append([])
    for box in boxes[level]:
        levelGround[level].extend(box[0])
        levelWall[level].extend(box[1])
