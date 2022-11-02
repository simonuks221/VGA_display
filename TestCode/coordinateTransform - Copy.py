from turtle import circle
import pygame
import numpy as np
from math import *
import random

RGBrandom = [[255, 0, 0], [255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 0, 255], [
    0, 0, 255], [255, 255, 0], [255, 255, 0], [0, 255, 255], [0, 255, 255]]


def bLineOG(x0, y0, x1, y1, screen, color):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    dx = abs(x1 - x0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    dy = -abs(y1 - y0)
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    error = dx + dy

    while True:
        pygame.draw.circle(screen, color, (x0, y0), 1)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy


def bLine(x0, y0, x1, y1, oldY, screen):
    x0 = int(x0)
    y0 = int(y0)
    x1 = int(x1)
    y1 = int(y1)

    # lastY = y0

    dx = abs(x1 - x0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    dy = -abs(y1 - y0)
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    error = dx + dy

    while True:

        if int(y0) == oldY:
            break

        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy
    return x0, y0


def takeSecond(elem):  # for sorting stuff
    return elem[1]


def bTriangle(P1, P2, P3, screen, color):

    Phigh = 0
    Pmid = 0
    Plow = 0

    P = [P1, P2, P3]
    P.sort(key=takeSecond)
    Phigh = P[2]
    Pmid = P[1]
    Plow = P[0]

    for newY in range(int(Phigh[1]), int(Pmid[1]), -1):
        xx1, yy1 = bLine(int(Phigh[0]), int(Phigh[1]), int(
            Plow[0]), int(Plow[1]), int(newY), screen)
        xx2, yy2 = bLine(int(Phigh[0]), int(Phigh[1]), int(
            Pmid[0]), int(Pmid[1]), int(newY), screen)
        bLineOG(xx1, yy1, xx2, yy2, screen, color)

    if Plow[1] != Phigh[1]:
        P4 = [Phigh[0] +
              ((Pmid[1]-Phigh[1])/(Plow[1]-Phigh[1])) * (Plow[0]-Phigh[0]), Pmid[1]]
    else:
        P4 = Pmid

    for newY in range(int(Pmid[1]), int(Plow[1]), -1):
        xx1, yy1 = bLine(int(P4[0]), int(P4[1]), int(
            Plow[0]), int(Plow[1]), int(newY), screen)
        xx2, yy2 = bLine(int(Pmid[0]), int(Pmid[1]), int(
            Plow[0]), int(Plow[1]), int(newY), screen)

        bLineOG(xx1, yy1, xx2, yy2, screen, color)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# all the cube vertices


scale = 100

# xyz
c = [4000, 5000, 0]  # camera position
# o = [0, -0.05, 0]  # orientation of camera
o = [0, 0, 0]  # orientation of camera
e = [800, 600, 1]  # display surface 1-90laipsniu 2.8 - 48laipsniai

points = []
# clockwise

# down
'''points.append([1, 200, 10])
points.append([200, 200, 10])
points.append([200, 200, 20])

points.append([200, 200, 20])
points.append([1, 200, 20])
points.append([1, 200, 10])

# back
points.append([1, 200, 20])
points.append([200, 1, 20])
points.append([1, 1, 20])


points.append([200, 1, 20])
points.append([1, 200, 20])
points.append([200, 200, 20])


# left
points.append([1, 1, 10])
points.append([1, 200, 10])
points.append([1, 1, 20])

points.append([1, 1, 20])
points.append([1, 200, 10])
points.append([1, 200, 20])
'''
# Right
'''points.append([200, 1, 10])
points.append([200, 1, 20])
points.append([200, 200, 20])

points.append([200, 1, 10])
points.append([200, 200, 20])
points.append([200, 200, 10])'''


# front
points.append([1, 200, 10])
points.append([1, 1, 10])
points.append([200, 1, 10])

points.append([200, 1, 10])
points.append([200, 200, 10])
points.append([1, 200, 10])


# points.append([200, 10, 100])


M = 360
circleIndex = 0
playerSpeed = 5

clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            c[2] += playerSpeed
        if pressed[pygame.K_s]:
            c[2] -= playerSpeed
        if pressed[pygame.K_a]:
            c[0] -= playerSpeed
        if pressed[pygame.K_d]:
            c[0] += playerSpeed
        if pressed[pygame.K_z]:
            c[1] -= playerSpeed
        if pressed[pygame.K_x]:
            c[1] += playerSpeed

        if pressed[pygame.K_q]:
            e[2] -= 5
        if pressed[pygame.K_e]:
            e[2] += 5
        print(2 * atan(1/e[2]))

        if pressed[pygame.K_UP]:
            o[0] += 0.1/180*pi
        if pressed[pygame.K_DOWN]:
            o[0] -= 0.1/180*pi

        if pressed[pygame.K_RIGHT]:
            o[1] += 1/180*pi
        if pressed[pygame.K_LEFT]:
            o[1] -= 1/180*pi

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    screen.fill(WHITE)
    drawPoints = []

    circleIndex += 0.05
    if circleIndex == 46:
        circleIndex = 0
    circleRadius = 10

    #e[2] += 1
    #e[0] += 10
    #e[1] += 1
    #e[2] = 20
    #c[0] -= 10
    #o[0] += 0.001
   # c[0] = sin(circleIndex / 180 * pi) * circleRadius*100
    # c[2] = cos(circleIndex / 180 * pi) * circleRadius*10
    calc3DPoints = []
    for i in range(0, len(points), 3):
        temp3Dpoints = []
        for ii in range(0, 3):
            x = points[ii+i][0] - c[0]
            y = points[ii+i][1] - c[1]
            z = points[ii+i][2] - c[2]
            cx = cos(o[0])
            cy = cos(o[1])
            cz = cos(o[2])
            sx = sin(o[0])
            sy = sin(o[1])
            sz = sin(o[2])

            dx = cy*(sz * y + cz * x) - sy*z
            dy = sx*(cy * z + sy*(sz*y+cz*x)) + cx*(cz*y-sz*x)
            dz = cx*(cy*z+sy*(sz*y+cz*x)) - sx*(cz*y-sz*x)

            fx = dx + dz*e[0]/e[2]
            fy = dy + dz*e[1]/e[2]
            fw = dz*1/e[2]

            if dz <= 0:  # dont render, behind camera
                break
            temp3Dpoints.append([fx, fy, fw])
        # calc normals
        if len(temp3Dpoints) == 3:
            Ax = temp3Dpoints[1][0] - temp3Dpoints[0][0]
            Ay = temp3Dpoints[1][1] - temp3Dpoints[0][1]
            Az = temp3Dpoints[1][2] - temp3Dpoints[0][2]
            Bx = temp3Dpoints[2][0] - temp3Dpoints[0][0]
            By = temp3Dpoints[2][1] - temp3Dpoints[0][1]
            Bz = temp3Dpoints[2][2] - temp3Dpoints[0][2]

            Nx = Ay * Bz - Az*By
            Ny = Az * Bx - Ax*Bz
            Nz = Ax * By - Ay*Bx
            # if Nz > 0:
            if True:
                calc3DPoints.append(temp3Dpoints[0])
                calc3DPoints.append(temp3Dpoints[1])
                calc3DPoints.append(temp3Dpoints[2])

    for i in calc3DPoints:
        bx = i[0]/i[2]
        by = i[1]/i[2]

        if bx < 0 or by < 0 or bx > 800 or by > 600:
            continue
        # pygame.draw.circle(screen, RED, (a[0] * scale, a[1]*scale), 5)
        drawPoints.append([bx, by])

    for i in range(0, len(drawPoints)):
        pygame.draw.circle(
            screen, RED, (drawPoints[i][0], drawPoints[i][1]), 5)

    colorIndex = 0
    for i in range(2, len(drawPoints), 3):
        bTriangle(drawPoints[i], drawPoints[i-1],
                  drawPoints[i-2], screen, RGBrandom[colorIndex])
        colorIndex += 1
    pygame.display.update()
    pygame.time.delay(300)
    # pygame.time.delay(1)
