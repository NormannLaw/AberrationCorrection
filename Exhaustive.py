import numpy as np
import math
import cv2 as cv
import screeninfo


def drawline_rotation(mat, start, rotation, grayscale):
    # Calculate coordinates of the start and end points
    # take row as x, downward direction is positive
    # take col as y, rightward direction is positive
    start_x = start[0] + 0.5
    start_y = start[1] + 0.5

    if rotation != math.pi / 2 or rotation != 3 * math.pi / 2:
        # get slope from rotation
        k = math.tan(rotation)

    # start filling the line, start with an x coordinate
    x = start_x
    y = start_y

    if rotation > 0 and rotation <= math.pi / 4 or rotation > math.pi and rotation <= 5 * math.pi / 4:

        while x <= mat.shape[0] - 0.5 and y <= mat.shape[1] - 0.5 and x >= 0 and y >= 0:

            # calculate the corresponding y coordinate
            y = start_y + k * (x - start_x)

            # find the nearest pixel centre and fill the pixel with grayscale value
            fill_y = math.floor(y)
            fill_x = math.floor(x)

            if fill_y > mat.shape[1] - 0.5:
                fill_y = mat.shape[1] - 1

            if fill_y < 0:
                fill_y = 0

            mat[fill_x][fill_y] = grayscale

            # proceed to next x value
            # make sure starting point on edge
            if start[0] == 0 or start[1] == 0:
                x += 1
            else:
                x -= 1

    elif rotation > math.pi / 4 and rotation < math.pi / 2 or rotation > 5 * math.pi / 4 and rotation < 3 * math.pi / 2:

        while (x <= mat.shape[0] - 0.5 and y <= mat.shape[1] - 0.5 and x >= 0 and y >= 0):

            x = start_x + (y - start_y) / k

            fill_y = math.floor(y)
            fill_x = math.floor(x)

            if fill_x > mat.shape[0] - 0.5:
                fill_x = mat.shape[0] - 1

            if fill_x < 0:
                fill_x = 0

            mat[fill_x][fill_y] = grayscale

            if start[0] == 0 or start[1] == 0:
                y += 1
            else:
                y -= 1

    elif rotation > math.pi / 2 and rotation <= 3 * math.pi / 4 or rotation > 3 * math.pi / 2 and rotation <= 7 * math.pi / 4:

        while (x <= mat.shape[0] - 0.5 and y <= mat.shape[1] - 0.5 and x >= 0 and y >= 0):

            x = start_x + (y - start_y) / k

            fill_y = math.floor(y)
            fill_x = math.floor(x)

            if fill_x > mat.shape[0] - 0.5:
                fill_x = mat.shape[0] - 1

            if fill_x < 0:
                fill_x = 0

            mat[fill_x][fill_y] = grayscale

            if start[0] == mat.shape[0] - 1 or start[1] == 0:
                y += 1
            else:
                y -= 1

    elif rotation > 3 * math.pi / 4 and rotation < math.pi or rotation > 7 * math.pi / 4 and rotation < 2 * math.pi:

        while (x <= mat.shape[0] - 0.5 and y <= mat.shape[1] - 0.5 and x >= 0 and y >= 0):

            y = start_y + k * (x - start_x)

            fill_y = math.floor(y)
            fill_x = math.floor(x)

            if fill_y > mat.shape[1] - 0.5:
                fill_y = mat.shape[1] - 1

            if fill_y < 0:
                fill_y = 0

            mat[fill_x][fill_y] = grayscale

            if start[0] == 0 or start[1] == mat.shape[1] - 1:
                x += 1
            else:
                x -= 1

    elif rotation == 0 or rotation == math.pi:
        # fix x (row number)
        fill_x = 0
        # start with the starting col
        fill_y = start[1]
        # fill all pixels
        while (fill_x < mat.shape[0]):
            mat[fill_x][fill_y] = grayscale
            fill_x += 1



    # if slope goes to infinity
    elif rotation != math.pi / 2 or rotation != 3 * math.pi / 2:
        # fix x (row number)
        fill_x = start[0]

        fill_y = 0
        # fill all pixels
        while (fill_y < mat.shape[1]):
            mat[fill_x][fill_y] = grayscale
            fill_y += 1


# Python testing version
def blazing_helper1(mat, rotation, width):
    grayscale = 0

    if rotation == math.pi or rotation == 0:
        increment = 1 / width
        col = 0

        for col in range(0, mat.shape[1]):
            if grayscale > 1:
                grayscale = 0
            drawline_rotation(mat, [0, col], 0, grayscale)
            grayscale += increment

    elif rotation == math.pi / 2 or rotation == 3 * math.pi / 2:
        increment = 1 / width
        row = 0

        for row in range(0, mat.shape[0]):
            if grayscale > 1:
                grayscale = 0
            drawline_rotation(mat, [row, 0], math.pi / 2, grayscale)
            grayscale += increment

    elif (rotation > 0 and rotation < math.pi / 2) or (rotation > math.pi and rotation < 3 * math.pi / 2):
        sin = abs(math.sin(rotation))
        cos = abs(math.cos(rotation))

        left_width = width / sin
        up_width = width / cos

        increment = 1 / width
        left_increment = increment * sin
        up_increment = increment * cos

        for row in range(0, mat.shape[0]):
            if grayscale > 1:
                grayscale = 0
            drawline_rotation(mat, [row, 0], rotation, grayscale)
            grayscale += left_increment

        grayscale = 1

        for col in range(1, mat.shape[1]):
            if grayscale < 0:
                grayscale = 1
            drawline_rotation(mat, [0, col], rotation, grayscale)
            grayscale -= up_increment

    else:
        sin = abs(math.sin(rotation))
        cos = abs(math.cos(rotation))

        up_width = width / cos
        right_width = width / sin

        increment = 1 / width
        up_increment = increment * cos
        right_increment = increment * sin

        col = mat.shape[1]
        while col >= 0:
            if grayscale > 1:
                grayscale = 0
            drawline_rotation(mat, [0, col], rotation, grayscale)
            grayscale += up_increment
            col -= 1

        grayscale = 1
        for row in range(1, mat.shape[0]):
            if grayscale < 0:
                grayscale = 1
            drawline_rotation(mat, [row, mat.shape[1] - 1], rotation, grayscale)
            grayscale -= right_increment


def add_mat(new_mat, big_mat, up_left):
    for row in range(up_left[0], up_left[0] + new_mat.shape[0]):
        for col in range(up_left[1], up_left[1] + new_mat.shape[1]):
            big_mat[row][col] = new_mat[row - up_left[0]][col - up_left[1]]


def try_next_mode(new_mat, big_mat, up_left, rotation, max_width):
    width = 10

    while width <= max_width:
        blazing_helper1(new_mat, rotation, width)
        add_mat(new_mat, big_mat, up_left)

        cv.imshow('SLM', big_mat)

        cv.waitKey(50)

        width += 10


def try_all_modes(n_row, n_col, big_row, big_col, rotation_increment, max_width):
    up_left = [0, 0]
    screen_id = 0

    big_mat = np.zeros((big_row, big_col))

    iteration = int((big_row * big_col) / (n_row * n_col))

    max_rotation = int(2 * math.pi / rotation_increment + 1)

    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]

    window_name = 'SLM'
    cv.namedWindow(window_name, cv.WND_PROP_FULLSCREEN)
    cv.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv.setWindowProperty(window_name, cv.WND_PROP_FULLSCREEN,
                         cv.WINDOW_FULLSCREEN)

    for i in range(0, iteration):

        new_mat = np.zeros((n_row, n_col))

        for rotation_index in range(0, max_rotation):
            rotation = rotation_index * rotation_increment
            try_next_mode(new_mat, big_mat, up_left, rotation, max_width)

        if up_left[1] + n_col >= big_mat.shape[1]:
            up_left[0] += n_row
            up_left[1] = 0

        else:
            up_left[1] += n_col

    while cv.waitKey(0) != 27:
        pass


max_width = 200
rotation_increment = 0.25 * math.pi
try_all_modes(108, 192, 1080, 1920, rotation_increment, max_width)

