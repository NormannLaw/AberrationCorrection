import cv2 as cv
import sys
import numpy
import math

def read_img(path):
    
    img = cv.imread(path, 0)

    return img

def inside_circle(point, centre, radius):
    distance_sqrd = (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2
    radius_sqrd = radius ** 2
    if distance_sqrd <= radius_sqrd:
        return True
    else:
        return False

def get_score(img, centre, radius):
    circle_area = math.pi * (radius ** 2)
    ideal = circle_area * 255
    in_circle = 0
    out_circle = 0

    total_row = len(img)
    total_col = len(img[0])

    total_area = total_col * total_row

    for row in range(0, total_row):
        for col in range(0, total_col):
            if inside_circle([row, col], centre, radius):
                in_circle += img[row][col]
            else:
                out_circle += img[row][col]

    score = (in_circle - out_circle) / circle_area

    return score

def find_optimised(img, centre, initial_radius, max_radius):
    score = -math.inf

    for radius in range(initial_radius, max_radius + 1):
        current_score = get_score(img, centre, radius)

        if current_score > score:
            score = current_score
            recorded_radius = radius

    return_me = [recorded_radius, score]

    return return_me


path1 = r'C:\Users\mluo\CizmarImplementation\Airy_Disk_Example1.png'
path2 = r'C:\Users\mluo\CizmarImplementation\Airy_Disk_Example2.png'
path3 = r'C:\Users\mluo\CizmarImplementation\Airy_Disk_Example3.png'
path4 = r'C:\Users\mluo\CizmarImplementation\Airy_Disk_Example4.png'

img1 = read_img(path1)
img2 = read_img(path2)
img3 = read_img(path3)
img4 = read_img(path4)

result1 = find_optimised(img1,[72,78], 10, 60)
result2 = find_optimised(img2,[77,68], 10, 60)
result3 = find_optimised(img3,[78,78], 10, 60)
result4 = find_optimised(img4,[78,67], 10, 60)

print('Example1: ' + str(result1[0]) + ' ' + str(result1[1]) + '\n')
print('Example2: ' + str(result2[0]) + ' ' + str(result2[1]) + '\n')
print('Example3: ' + str(result3[0]) + ' ' + str(result3[1]) + '\n')
print('Example4: ' + str(result4[0]) + ' ' + str(result4[1]) + '\n')
#print(get_score(img, [70, 70], 40))






