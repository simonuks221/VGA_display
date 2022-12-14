import pygame
import numpy as np
from math import *
import random
import math

zbuffer = [[1000]*600 for i in range(800)]


def getMiddleZ(Phigh, Pmid, Plow):
    if (Phigh[1] - Plow[1]) == 0:
        return Phigh[2]
    return -(Phigh[1]-Pmid[1])/(Phigh[1] - Plow[1]) * \
            (Phigh[2] - Plow[2]) + Phigh[2]


def TextureCoords(R1, R2, R3, P):
    detT = (R2[1]-R3[1])*(R1[0]-R3[0])+(R3[0]-R2[0])*(R1[1]-R3[1])
    l1 = ((R2[1]-R3[1])*(P[0]-R3[0])+(R3[0]-R2[0])*(P[1]-R3[1]))/detT
    l2 = ((R3[1]-R1[1])*(P[0]-R3[0])+(R1[0]-R3[0])*(P[1]-R3[1]))/detT
    l3 = 1 - l1 - l2
    if R1[2] == 0 or R2[2] == 0 or R3[2] == 0:
        detB = 1
        B1 = 1
        B2 = 1
        B3 = 1
    else:
        detB = l1/R1[2]+l2/R2[2]+l3/R3[2]
        B1 = (l1/R1[2])/detB  # depth shit
        B2 = (l2/R2[2])/detB
        B3 = (l3/R3[2])/detB

    u = B1 * R1[3] + B2 * R2[3] + B3 * R3[3]
    try:
        v = B1 * R1[4] + B2 * R2[4] + B3 * R3[4]
    except:
        print(R1, R2, R3)
    if u < 0 or v < 0:
        return (0, 0)
    if u > 1 or v > 1:
        return (0, 0)
    return (u, v)


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

    a1 = (line1[0][1] - line1[1][1])/(line1[0][0] - line1[1][0])  # y1-y2/x1-x2
    b1 = line1[0][1]-(a1*line1[0][0])  # y1 - ax

    if givenX != -1:  # find y
        x = givenX
        y = b1
    else:  # find x
        y = givenY
        x = (givenY - b1)/a1
    return (int(x), int(y))


def drawPixel(x, y, z, V1, V2, V3, screen):
    global zbuffer
    if zbuffer[x][y] > z:
        u, v = TextureCoords(V1, V2, V3, (x, y))
        color = (255 * z/100, 0, 0)
        if color[0] > 255:
            color = (255, 0, 0)
        pygame.draw.circle(screen, color, (x, y), 1)
        zbuffer[x][y] = z


def line3DDraw(P0, P1, screen, V1, V2, V3):
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


def line3DSides(P0, P1, lastY):
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
            if (err_1 > 0):

                py += y_inc
                err_1 -= dx2
            if (err_2 > 0):
                pz += z_inc
                err_2 -= dx2

            err_1 += dy2
            err_2 += dz2
            px += x_inc
            if lastY == py + y0:
                break

    elif ((m >= l) and (m >= n)):
        err_1 = dx2 - m
        err_2 = dz2 - m
        for i in range(0, m):
            if (err_1 > 0):
                px += x_inc
                err_1 -= dy2

            if (err_2 > 0):
                pz += z_inc
                err_2 -= dy2

            err_1 += dx2
            err_2 += dz2
            py += y_inc
            if lastY == py + y0:
                break

    else:
        err_1 = dy2 - n
        err_2 = dx2 - n
        for i in range(0, n):
            if (err_1 > 0):
                py += y_inc
                err_1 -= dz2
            if (err_2 > 0):
                px += x_inc
                err_2 -= dz2
            err_1 += dy2
            err_2 += dx2
            pz += z_inc
            if lastY == py + y0:
                break
    return px + x0, py + y0, pz + z0


def takeSecond(elem):  # for sorting stuff
    return elem[1]


def bTriangle(P1, P2, P3, screen):

    Phigh = 0
    Pmid = 0
    Plow = 0

    P = [P1, P2, P3]
    P.sort(key=takeSecond)

    Phigh = P[2]
    Pmid = P[1]
    Plow = P[0]

    for newY in range(int(Phigh[1]), int(Pmid[1]), -1):
        xx1, yy1, zz1 = line3DSides(Phigh, Plow, int(newY))
        xx2, yy2, zz2 = line3DSides(Phigh, Pmid, int(newY))
        line3DDraw((xx1, yy1, zz1), (xx2, yy2, zz2), screen, P1, P2, P3)

    if Plow[1] != Phigh[1]:
        newZ = getMiddleZ(Phigh, Pmid, Plow)
        P4 = [Phigh[0] +
              ((Pmid[1]-Phigh[1])/(Plow[1]-Phigh[1])) * (Plow[0]-Phigh[0]), Pmid[1], newZ]  # 0 - z coord
    else:
        P4 = Pmid

    for newY in range(int(Pmid[1]), int(Plow[1]), -1):
        xx1, yy1, zz1 = line3DSides(P4, Plow, int(newY))
        xx2, yy2, zz2 = line3DSides(Pmid, Plow, int(newY))
        line3DDraw((xx1, yy1, zz1), (xx2, yy2, zz2), screen, Phigh, Pmid, Plow)


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
points.append([20, 0, 10])
points.append([20, 0, 30])
points.append([20, 20, 10])

points.append([20, 0, 30])
points.append([20, 20, 30])
points.append([20, 20, 10])

tcoords.append((0, 0))
tcoords.append((1, 0))
tcoords.append((0, 1))

tcoords.append((1, 0))
tcoords.append((1, 1))
tcoords.append((0, 1))

# front
points.append([0, 0, 10])
points.append([20, 0, 10])
points.append([0, 20, 10])

points.append([20, 0, 10])
points.append([20, 20, 10])
points.append([0, 20, 10])

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

ccx = 1
ccy = 1  # camerapos
ccz = 1

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
            ccz += playerSpeed
        if pressed[pygame.K_s]:
            ccz -= playerSpeed
        if pressed[pygame.K_a]:
            ccx -= playerSpeed
        if pressed[pygame.K_d]:
            ccx += playerSpeed
        if pressed[pygame.K_z]:
            ccy -= playerSpeed
        if pressed[pygame.K_x]:
            ccy += playerSpeed

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

    screen.fill((255, 255, 255))
    # drawining stuff

    for i in range(0, len(points), 3):
        drawPoints = []
        Z = 1000
        for yy in range(0, 3):
            x = points[i+yy][0] - ccx
            # print(points[i+yy])
            y = points[i+yy][1] - ccy
            z = points[i+yy][2] - ccz
            cx = cos(anglex)
            cy = cos(angley)
            cz = cos(anglez)
            sx = sin(anglex)
            sy = sin(angley)
            sz = sin(anglez)

            dx = cy*(sz * y + cz * x) - sy*z
            dy = sx*(cy * z + sy*(sz*y+cz*x)) + cx*(cz*y-sz*x)
            dz = cx*(cy*z+sy*(sz*y+cz*x)) - sx*(cz*y-sz*x)

            if dz <= 0:  # behind camera
                drawPoints.clear()
                break
            bx = ez/dz*dx + ex
            by = ez/dz*dy + ey
            print(points[i+yy], bx, by, dz, dx, dy)
            drawPoints.append([bx, by, dz, tcoords[i+yy][0], tcoords[i+yy][1]])

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
                    print(goodvertex1, badvertex0)
                    newz0 = getMiddleZ(goodvertex0, (newx0, newy0), badvertex0)

                    newz1 = getMiddleZ(goodvertex1, (newx1, newy1), badvertex0)
                    print(newz1)
                    bTriangle(goodvertex0, (newx0, newy0, newz0, 1, 1),
                              goodvertex1, screen)
                    bTriangle((newx1, newy1, 100, 1, 1), (newx0, newy0, newz1, 1, 1),
                              goodvertex1, screen)
                    continue
                elif verticiesOutside == 2:  # 2 vertices over board, one good
                    newx0, newy0 = lineIntersection(
                        (goodvertex0, badvertex0), -1, -1)
                    newz0 = getMiddleZ(goodvertex0, (newx0, newy0), badvertex0)
                    newx1, newy1 = lineIntersection(
                        (goodvertex0, badvertex1), -1, -1)
                    newz1 = getMiddleZ(goodvertex0, (newx1, newy1), badvertex1)
                    bTriangle(goodvertex0, (newx0, newy0, newz0, 1, 1),
                              (newx1, newy1, newz1, 1, 1), screen)

                    continue
                elif verticiesOutside == 3:
                    continue
                else:  # all good
                    bTriangle(drawPoints[0], drawPoints[1],
                              drawPoints[2], screen)

    pygame.display.update()
