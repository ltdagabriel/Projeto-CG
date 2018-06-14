# -*- coding: utf-8 -*-
import sys
from objloader import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame import *
import math


class Main:
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    angleY = 0
    angleX = 0
    cube_angle = 0

    def __init__(self):
        pygame.init()
        self.viewport = (1280, 650)
        glutInitWindowPosition(100, 0)
        pygame.display.set_mode(self.viewport, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("PROJETO CGR")

        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

        # ---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0, 0, -10]

        self.init()

        self.pokebola = OBJ("pokebola.obj", swapyz=True)

        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        done = False
        view = False
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move_left()
                    self.left_key = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move_right()
                    self.right_key = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.move_forward()
                    self.up_key = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.move_back()
                    self.down_key = True
                elif event.key == pygame.K_0:
                    view = not view

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.keyup()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.keyup()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.keyup()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.keyup()

        self.update()
        if view:
            self.divideViewport()
        else:
            self.display()

        pygame.display.flip()
        clock.tick(30)

        if not done:
            self.loop()

        pygame.quit()

    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False

    def divideViewport(self):
        print("Entrou")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # /** viewport do canto superior esquerdo **/
        glColor3f(0.0, 0.0, 1.0)
        glViewport(0, 0, 1000, 700)
        glColor3f(0.0, 0.0, 1.0)

        # VIEWPORT GRANDE DA ESQUERDA
        glViewport(0, 0, 800, 650)

        glMatrixMode(GL_PROJECTION)  # //define que a matrix é a de projeção
        glLoadIdentity()  # //carrega a matrix de identidade
        gluPerspective(90.0, 1280 / float(650), 1, 100.0)
        self.display()

        glMatrixMode(GL_MODELVIEW)  # //matrix em uso: modelview
        glLoadIdentity()

        # VIEWPORT DO CANTO INFERIOR DIREITO
        glViewport(800, 0, 480, 325)
        glMatrixMode(GL_PROJECTION)  # //define que a matrix é a de projeção
        glLoadIdentity()  # //carrega a matrix de identidade
        gluPerspective(90.0, 1280 / float(650), 1, 100.0)

        glMatrixMode(GL_MODELVIEW)  # //matrix em uso: modelview
        glLoadIdentity()
        self.display()

        # VIEWPORT DO CANTO SUPERIOR DIREITO
        glViewport(800, 325, 480, 325)
        glMatrixMode(GL_PROJECTION)  # //define que a matrix é a de projeção
        glLoadIdentity()  # //carrega a matrix de identidade
        gluPerspective(90.0, 1280 / float(650), 1, 100.0)

        self.display()
        glMatrixMode(GL_MODELVIEW)  # //matrix em uso: modelview
        glLoadIdentity()

    def move_forward(self):
        self.coordinates[2] += 0.1 * math.cos(math.radians(self.angleY))
        self.coordinates[0] -= 0.1 * math.sin(math.radians(self.angleY))

    def move_back(self):
        self.coordinates[2] -= 0.1 * math.cos(math.radians(self.angleY))
        self.coordinates[0] += 0.1 * math.sin(math.radians(self.angleY))

    def move_left(self):
        self.coordinates[0] += 0.1 * math.cos(math.radians(self.angleY))
        self.coordinates[2] += 0.1 * math.sin(math.radians(self.angleY))

    def move_right(self):
        self.coordinates[0] -= 0.1 * math.cos(math.radians(self.angleY))
        self.coordinates[2] -= 0.1 * math.sin(math.radians(self.angleY))

    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()

        self.cube_angle = 0 if self.cube_angle >= 360 else self.cube_angle + 1

    def init(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = self.viewport
        gluPerspective(90.0, width / float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

    def plano(self):

        # Linha Z
        glPushMatrix()

        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1000)
        glEnd()
        glColor3f(0, 0, 1)

        glPopMatrix()

        # Linha Y
        glPushMatrix()

        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1000, 0)
        glEnd()
        glColor3f(0, 1, 0)

        glPopMatrix()

        # Linha X
        glPushMatrix()

        glBegin(GL_LINE_LOOP)
        glVertex3f(0, 0, 0)
        glVertex3f(1000, 0, 0)
        glEnd()
        glColor3f(0, 1, 1)

        glPopMatrix()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.7, 0.9, 1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        luzAmbiente = [0.1, 0.1, 0.1, 1.0]
        luzDifusa = [0.7, 0.7, 0.7, 1.0]
        luzEspecular = [1.0, 1.0, 1.0, 1.0]
        posicaoLuz = [0.0, 10.0, 0.0, 1.0]

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luzAmbiente)
        # glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente)
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa)
        # glLightfv(GL_LIGHT0, GL_SPECULAR, luzEspecular)
        # glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz)

        # Add positioned light:
        # glLightfv(GL_LIGHT1, GL_SPECULAR, (0.9, 0.9, 0.9, 0.8))
        # glLightfv(GL_LIGHT1, GL_AMBIENT, (0.65, 0.65, 0.65, 0.9))
        # glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.65, 0.65, 0.65, 0.9))
        # glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 0.2))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 0.9))

        # gluLookAt(camera.x, camera.y, camera.z,  lookat.x, lookat.y, lookat.z, 0, 1, 0)

        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])

        glPushMatrix()

        # coloca a pokebola acima do chao
        glTranslatef(0, 2, 1)
        # faz a pokebola ficar girando
        glRotatef(self.cube_angle, 0, 1, 0)
        glRotatef(45, 1, 0, 0)
        glTranslatef(0, 0, -1)
        glCallList(self.pokebola.gl_list)

        glPopMatrix()

        self.plano()


if __name__ == '__main__':
    Main()
