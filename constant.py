player_x_size = 46
player_y_size = 50

num = 3   # number of levels

def box(x, y, length, height):   # return [boxGrounds, boxWalls]
	return [[[x, x + length, y], [x, x + length, y + height]], [[y, y + height, x], [y, y + height, x + length]]]

boxes = []

#  level 1
boxes.append([box(0, 350, 500, 130), box(600, 350, 40, 130)])

#  level 2
boxes.append([box(0, 350, 640, 130)])

#  level 3
boxes.append([box(0, 350, 300, 130), box(150, 300, 100, 50), box(300, 200, 150, 50), box(400, 320, 240, 160)])

levelGround = []
levelWall = []

for level in range(num):
    levelGround.append([])
    levelWall.append([])
    for box in boxes[level]:
        levelGround[level].extend(box[0])
        levelWall[level].extend(box[1])
