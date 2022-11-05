import pygame
import numpy as np
from math import *
import random
import math

zbuffer = [[1000]*600 for i in range(800)]


def TextureCoords(R1, R2, R3, P):
    detT = (R2[1]-R3[1])*(R1[0]-R3[0])+(R3[0]-R2[0])*(R1[1]-R3[1])
    l1 = ((R2[1]-R3[1])*(P[0]-R3[0])+(R3[0]-R2[0])*(P[1]-R3[1]))/detT
    l2 = ((R3[1]-R1[1])*(P[0]-R3[0])+(R1[0]-R3[0])*(P[1]-R3[1]))/detT
    l3 = 1 - l1 - l2
    detB = l1/R1[2]+l2/R2[2]+l3/R3[2]
    B1 = (l1/R1[2])/detB
    B2 = (l2/R2[2])/detB
    B3 = (l3/R3[2])/detB
    #u = l1 * R1[3] + l2 * R2[3] + l3 * R3[3]
    #v = l1 * R1[4] + l2 * R2[4] + l3 * R3[4]

    u = B1 * R1[3] + B2 * R2[3] + B3 * R3[3]
    v = B1 * R1[4] + B2 * R2[4] + B3 * R3[4]
    if u < 0 or v < 0:
        return (0, 0)
    if u > 1 or v > 1:
        #print("ERROR: OVER 1 COLOR", u, v)
        return (0, 0)
    return (u, v)

#print(k1, k1)
# print(k2, k2)


def lineIntersection(line1, givenX=-1, givenY=-1):
    # print(line1)
    if line1[1][0] < 0:
        givenX = 0
    elif line1[1][1] < 0:
        givenY = 0
    elif line1[1][0] >= 800:
        givenX = 800-1
    elif line1[1][1] >= 600:
        givenY = 600-1

    if (line1[0][0] == line1[1][0]):
        if givenX != -1:  # find y
            return (int(givenX), int(line1[0][1]))
        else:  # find x
            return (int(line1[0][0]), int(givenY))
            return

    a1 = (line1[0][1] - line1[1][1])/(line1[0][0] - line1[1][0])  # y1-y2/x1-x2
    b1 = line1[0][1]-(a1*line1[0][0])  # y1 - ax

    if givenX != -1:  # find y
        x = givenX
        y = b1
    else:  # find x
        y = givenY
        x = (givenY - b1)/a1
       # x = (b2 - b1)/(a1+a2)
        #y = a1 * x + b1

    return (int(x), int(y))


def drawPixel(x, y, z, V1, V2, V3, screen):
    global zbuffer
    if zbuffer[x][y] > Z:
        u, v = TextureCoords(V1, V2, V3, (x, y))
        color = (0, 255 * v, 0)
        pygame.draw.circle(screen, color, (x, y), 1)
        zbuffer[x][y] = Z


def line3D(P0, P1, screen, V1, V2, V3):
    x0 = int(P0[0])
    y0 = int(P0[1])
    z0 = int(P0[2])
    x1 = int(P1[0])
    y1 = int(P1[1])
    z1 = int(P1[2])
    px = 0
    py = 0
    pz = 0

    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    if dx < 0:
        x_inc = -1
    else:
        x_inc = 1
    if dy < 0:
        y_inc = -1
    else:
        y_inc = 1
    if dz < 0:
        z_inc = -1
    else:
        z_inc = 1

    l = abs(dx)
    m = abs(dy)
    n = abs(dz)
    dx2 = l << 1
    dy2 = m << 1
    dz2 = n << 1

    if ((l >= m) and (l >= n)):
        err_1 = dy2 - l
        err_2 = dz2 - l
        for i in range(0, l):
           # for (i=0; i < l; i++) {
            # output -> getTileAt(point[0], point[1], point[2]) -> setSymbol(symbol)
            drawPixel(px + x0, py + y0, pz + z0, V1, V2, V3, screen)
            if (err_1 > 0):

                py += y_inc
                err_1 -= dx2
            if (err_2 > 0):
                pz += z_inc
                err_2 -= dx2

            err_1 += dy2
            err_2 += dz2
            px += x_inc

    elif ((m >= l) and (m >= n)):
        err_1 = dx2 - m
        err_2 = dz2 - m
        # for (i=0; i < m;i++) {
        # output -> getTileAt(point[0], point[1], point[2]) -> setSymbol(symbol)

        for i in range(0, m):
            drawPixel(px + x0, py + y0, pz + z0, V1, V2, V3, screen)
            if (err_1 > 0):
                px += x_inc
                err_1 -= dy2

            if (err_2 > 0):
                pz += z_inc
                err_2 -= dy2

            err_1 += dx2
            err_2 += dz2
            py += y_inc

    else:
        err_1 = dy2 - n
        err_2 = dx2 - n
        # for (i=0;i < n;i++) {
        #    output -> getTileAt(point[0], point[1], point[2]) -> setSymbol(symbol)

        for i in range(0, n):
            drawPixel(px + x0, py + y0, pz + z0, V1, V2, V3, screen)
            if (err_1 > 0):
                py += y_inc
                err_1 -= dz2
            if (err_2 > 0):
                px += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            pz += z_inc
    drawPixel(px + x0, py + y0, pz + z0, V1, V2, V3, screen)


def bLineOG(x0, y0, x1, y1, Z, screen, V1, V2, V3):
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
        drawPixel(x0, y0, Z, V1, V2, V3, screen)
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


def bLine(P0, P1, oldY, screen):
    x0 = int(P0[0])
    y0 = int(P0[1])
    x1 = int(P1[0])
    y1 = int(P1[1])

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


def bTriangle(P1, P2, P3, Z, screen):

    Phigh = 0
    Pmid = 0
    Plow = 0

    P = [P1, P2, P3]
    P.sort(key=takeSecond)

    Phigh = P[2]
    Pmid = P[1]
    Plow = P[0]

    for newY in range(int(Phigh[1]), int(Pmid[1]), -1):
        xx1, yy1 = bLine(Phigh,
                         Plow, int(newY), screen)
        xx2, yy2 = bLine(Phigh,
                         Pmid, int(newY), screen)
        bLineOG(xx1, yy1, xx2, yy2, Z, screen, P1, P2, P3)

    if Plow[1] != Phigh[1]:
        P4 = [Phigh[0] +
              ((Pmid[1]-Phigh[1])/(Plow[1]-Phigh[1])) * (Plow[0]-Phigh[0]), Pmid[1]]
    else:
        P4 = Pmid

    for newY in range(int(Pmid[1]), int(Plow[1]), -1):
        xx1, yy1 = bLine(P4,
                         Plow, int(newY), screen)
        xx2, yy2 = bLine(Pmid,
                         Plow, int(newY), screen)

        bLineOG(xx1, yy1, xx2, yy2, Z, screen, P1, P2, P3)


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection in pygame!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 1

circle_pos = [WIDTH/2, HEIGHT/2]  # x, y


points = []
tcoords = []

# clockwise
# back
'''points.append(np.matrix([0, 0, 30]))
points.append(np.matrix([0, 20, 30]))
points.append(np.matrix([20, 0, 30]))

points.append(np.matrix([20, 0, 30]))
points.append(np.matrix([0, 20, 30]))
points.append(np.matrix([20, 20, 30]))
'''

# Right
points.append(np.matrix([20, 0, 10]))
points.append(np.matrix([20, 0, 30]))
points.append(np.matrix([20, 20, 10]))

points.append(np.matrix([20, 0, 30]))
points.append(np.matrix([20, 20, 30]))
points.append(np.matrix([20, 20, 10]))

tcoords.append((0, 0))
tcoords.append((1, 0))
tcoords.append((0, 1))

tcoords.append((1, 0))
tcoords.append((1, 1))
tcoords.append((0, 1))

# front
points.append(np.matrix([0, 0, 10]))
points.append(np.matrix([20, 0, 10]))
points.append(np.matrix([0, 20, 10]))

points.append(np.matrix([20, 0, 10]))
points.append(np.matrix([20, 20, 10]))
points.append(np.matrix([0, 20, 10]))

tcoords.append((0, 0))
tcoords.append((1, 0))
tcoords.append((0, 1))

tcoords.append((1, 0))
tcoords.append((1, 1))
tcoords.append((0, 1))


# Left
'''points.append(np.matrix([0, 0, 10]))
points.append(np.matrix([0, 20, 10]))
points.append(np.matrix([0, 0, 30]))


points.append(np.matrix([0, 0, 30]))
points.append(np.matrix([0, 20, 10]))
points.append(np.matrix([0, 20, 30]))

# Top
points.append(np.matrix([0, 0, 10]))
points.append(np.matrix([0, 0, 30]))
points.append(np.matrix([20, 0, 10]))


points.append(np.matrix([0, 0, 30]))
points.append(np.matrix([20, 0, 30]))
points.append(np.matrix([20, 0, 10]))'''


'''points.append(np.matrix([-10, 10, 10]))
points.append(np.matrix([-10, -10, 20]))
points.append(np.matrix([10, -10, 20]))
points.append(np.matrix([10, 10, 20]))
points.append(np.matrix([-10, 10, 20]))'''


projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
])


projected_points = [
    [n, n] for n in range(len(points))
]


# def connect_points(i, j, points):
# print()
# pygame.draw.line(
#    screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))


cx = 0
cy = 0  # camerapos
cz = -50

ex = 100
ey = 100  # display surface
ez = 150

anglex = 0
angley = 0
anglez = 0

playerSpeed = 1

circleK = 360
K = 0

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for y in range(0, 600):
        for x in range(0, 800):
            zbuffer[x][y] = 1000
    if K == circleK:
        K = 0
    else:
        K += 1

    # cz = (cos(K/180*pi)) * 200
    # cx = (sin(K/180*pi)) * 200
    # myradians = math.atan2(0-cz, 0-cx)
    # print(angley)
    # angley = myradians - 0.78  # 45 degrees of something wrong
    # print(K)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            cz += playerSpeed
        if pressed[pygame.K_s]:
            cz -= playerSpeed
        if pressed[pygame.K_a]:
            cx -= playerSpeed
        if pressed[pygame.K_d]:
            cx += playerSpeed
        if pressed[pygame.K_z]:
            cy -= playerSpeed
        if pressed[pygame.K_x]:
            cy += playerSpeed

        if pressed[pygame.K_q]:
            anglez += 1/180*pi
        if pressed[pygame.K_e]:
            anglez -= 1/180*pi
        # print(2 * atan(1/e[2]))

        if pressed[pygame.K_UP]:
            anglex += 1/180*pi
        if pressed[pygame.K_DOWN]:
            anglex -= 1/180*pi

        if pressed[pygame.K_RIGHT]:
            angley += 1/180*pi
        if pressed[pygame.K_LEFT]:
            angley -= 1/180*pi

        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

    # update stuff

    rotation_z = np.matrix([
        [cos(anglez), -sin(anglez), 0],
        [sin(anglez), cos(anglez), 0],
        [0, 0, 1],
    ])

    rotation_y = np.matrix([
        [cos(angley), 0, sin(angley)],
        [0, 1, 0],
        [-sin(angley), 0, cos(angley)],
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(anglex), -sin(anglex)],
        [0, sin(anglex), cos(anglex)],
    ])

    # angle += 0.01

    screen.fill(WHITE)
    # drawining stuff

    for i in range(0, len(points), 3):
        drawPoints = []
        Z = 1000
        for y in range(0, 3):
            rotated2d = points[i + y].reshape((3, 1))
            carray = np.matrix([[cx], [cy], [cz]])
            rotated2d = rotated2d - carray
            rotated2d = np.dot(rotation_z, rotated2d)
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)

            dx = int(rotated2d[0][0])
            dy = int(rotated2d[1][0])
            dz = int(rotated2d[2][0])

            Z = dz

            if dz <= 0:  # behind camera
                drawPoints.clear()
                break
            bx = ez/dz*dx + ex
            by = ez/dz*dy + ey
            drawPoints.append([bx, by, dz, tcoords[i+y][0], tcoords[i+y][1]])

        if (len(drawPoints) == 3):
            X1 = (drawPoints[1][0] - drawPoints[0][0]) * \
                (drawPoints[1][1] + drawPoints[0][1])
            X2 = (drawPoints[2][0] - drawPoints[1][0]) * \
                (drawPoints[2][1] + drawPoints[1][1])
            X3 = (drawPoints[0][0] - drawPoints[2][0]) * \
                (drawPoints[0][1] + drawPoints[2][1])
            if X1 + X2 + X3 < 0:
                verticiesOutside = 0
                badvertex0 = 0
                badvertex1 = 0
                goodvertex0 = 0
                goodvertex1 = 0
                goodVerticies = 0
                for a in drawPoints:  # Clipping outside
                    if a[0] < 0 or a[1] < 0 or a[1] >= 600 or a[0] >= 800:
                        if verticiesOutside == 0:
                            badvertex0 = a
                        else:
                            badvertex1 = a
                        verticiesOutside += 1
                    else:
                        if goodVerticies == 0:
                            goodvertex0 = a
                            goodVerticies += 1
                        else:
                            goodvertex1 = a
                if verticiesOutside == 1:  # one overboard, two good
                    newx0, newy0 = lineIntersection(
                        (goodvertex0, badvertex0), -1, -1)
                    newx1, newy1 = lineIntersection(
                        (goodvertex1, badvertex0), -1, -1)
                    bTriangle(goodvertex0, (newx0, newy0), goodvertex1,  # nera teksturu koordinaciu cia ir toliau
                              Z, screen)
                    bTriangle((newx1, newy1), (newx0, newy0), goodvertex1,
                              Z, screen)
                    continue
                elif verticiesOutside == 2:  # 2 vertices over board, one good
                    newx0, newy0 = lineIntersection(
                        (goodvertex0, badvertex0), -1, -1)
                    newx1, newy1 = lineIntersection(
                        (goodvertex0, badvertex1), -1, -1)
                    bTriangle(goodvertex0, (newx0, newy0), (newx1, newy1),
                              Z, screen)

                    continue
                elif verticiesOutside == 3:
                    continue
                else:  # all good
                    bTriangle(drawPoints[0], drawPoints[1],
                              drawPoints[2], Z, screen)
                '''pygame.draw.circle(
                    screen, BLACK, (drawPoints[0][0], drawPoints[0][1]), 5)
                pygame.draw.circle(
                    screen, BLACK, (drawPoints[1][0], drawPoints[1][1]), 5)
                pygame.draw.circle(
                    screen, BLACK, (drawPoints[2][0], drawPoints[2][1]), 5)'''

    pygame.display.update()
