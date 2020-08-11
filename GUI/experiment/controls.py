import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import time

verticies = (
    (1, -.1, -1),
    (1, .1, -1),
    (-1, .1, -1),
    (-1, -.1, -1),
    (1, -.1, 1),
    (1, .1, 1),
    (-1, -.1, 1),
    (-1,.1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

def Kvadar():
    glBegin(GL_QUADS)
    for surface in surfaces:
        glColor3fv((1, 1, 1))
        for vertex in surface:
           glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0, 0, 0))
            glVertex3fv(verticies[vertex])                    
    glEnd()
 
def main():
    thrust = 0#percent

    rotateLeft=False#rotation is initially not moving
    rotateRight=False
    pitchUp=False#pitch is initially not moving
    pitchDown=False
    increaseThrust=False#thrust is initially not being increased
    decreaseThrust=False
    aDown=False#a is initially not being pressed
    dDown=False
    wDown=False
    sDown=False

    print("\n\nUse arrows or WASD to rotate and LSHIFT/SPACE to change thrust\n r to izravnati drona")
    #time.sleep(3)

    pygame.init()
    display = (800,600)
    simDisplay = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -6)

    glPushMatrix()#to save the current transformation

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    rotateLeft=True
                    if dDown:#if d is still being pressed don't rotate right anymore
                        rotateRight=False
                    aDown=True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    rotateRight=True
                    if aDown:
                        rotateLeft=False
                    dDown=True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pitchDown=True
                    if sDown:
                        pitchUp=False
                    wDown=True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pitchUp=True
                    if wDown:
                        pitchDown=False
                    sDown=True
                if event.key == pygame.K_UP:
                    print('fuck')
                    increaseThrust=True
                if event.key == pygame.K_DOWN:
                    print('fuck')
                    decreaseThrust=True
                if event.key == pygame.K_r:#izravnaj dron i resetiraj svoj referentni sustav (da yaw bude 0)
                    glPopMatrix() #to go back to the saved transformation
                    glPushMatrix() #to save transformation again


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    rotateLeft=False
                    if dDown:
                        rotateRight=True
                    aDown=False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    rotateRight=False
                    if aDown:
                        rotateLedt=True
                    dDown=False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    pitchDown = False
                    if sDown:
                        pichUp=True
                    wDown=False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    pitchUp = False
                    if wDown:
                        pitchUp=True
                    sDown=False
                if event.key == pygame.K_SPACE:
                    increaseThrust=False
                if event.key == pygame.K_LSHIFT:
                    decreaseThrust=False

        if rotateLeft:
            glRotatef(0.4, 0, 0, 1)
        if rotateRight:
            glRotatef(0.4, 0, 0, -1)
        if pitchUp:
            glRotatef(0.4, 1, 0, 0)
        if pitchDown:
            glRotatef(0.4, -1, 0, 0)
        if increaseThrust:
            thrust+=0.5
            if thrust>100:
                thrust=100
        if decreaseThrust:
            thrust-=0.5
            if thrust<0:
                thrust=0


        

        print("Thrust: " + str(thrust) + "%")


        #x = glGetDoublev(GL_MODELVIEW_MATRIX)
        #print(x)
    



        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Kvadar()
        pygame.display.flip()
        pygame.time.wait(10)


main()
