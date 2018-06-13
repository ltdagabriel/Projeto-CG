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
        self.screen = pygame.display.set_mode(self.viewport, DOUBLEBUF | OPENGL)
        pygame.display.set_gamma(1, 0, 0)
        pygame.display.set_caption("PROJETO CGR")

        self.font = pygame.font.SysFont("comicsansms", 24)

        # ---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0, 0, -10]

        self.init()

        self.pokebola = OBJ("pokebola.obj", swapyz=True)

        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        done = False

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
                    self.divideViewport()

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

        glMatrixMode(GL_PROJECTION)  # //define que a matrix é a de projeção
        glLoadIdentity()  # //carrega a matrix de identidade
        glOrtho(-3.0, 3.0, -3.0, 3.0, 1.0, 50.0)  # //define uma projeção ortogonal

        glMatrixMode(GL_MODELVIEW)  # //matrix em uso: modelview
        glLoadIdentity()

        # /** define a posicao da camera **/
        gluLookAt(0.0, 1.0, 0.0,  # //posição da câmera
                  0.0, 0.0, 0.0,  # //para onde a câmera aponta
                  0.0, 0.0, 1.0)  # //vetor view-up*/

        glColor3f(1.0, 0.0, 0.0)  # //altera o atributo de cor

    # glutWireTeapot(1.0); #// desenha o tea pot

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

    def rotateX(self, n):
        if self.angleY >= 360 or self.angleY <= -360:
            self.angleY = 0
        self.angleY += n

    def rotateY(self, n):
        if self.angleX >= 360 or self.angleX <= -360:
            self.angleX = 0
        self.angleX += n

    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()

        if self.cube_angle >= 360:
            self.cube_angle = 0
        else:
            self.cube_angle += 0.5

    def teapot(self):
        glRotatef(45, 1, 0, 0)
        glRotatef(self.cont, 0, 0, 1)
        glutWireTeapot(1)

        self.cont = 0 if self.cont == 360 else self.cont + 1

        glutPostRedisplay()

    def init(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glEnable(GL_LIGHT1)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # ativa textuta de arquivos mtl
        glEnable(GL_COLOR_MATERIAL)
        # ativa sombra de arquivos obj
        glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)

        # Reinicializa a cor de fundo
        glClearColor(1, 1, 1, 1)

        glMatrixMode(GL_PROJECTION)
        # Matriz de identidade
        glLoadIdentity()

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

    def desenha_objeto(self):
        glBegin(GL_TRIANGLES)
        glVertex2i(50, -50)
        glVertex2i(0, 50)
        glVertex2i(-50, -50)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex2i(-99, -99)
        glVertex2i(99, -99)
        glVertex2i(99, 99)
        glVertex2i(-99, 99)
        glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.7, 0.9, 1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        luzAmbiente = [0.8, 0.8, 0.8, 1.0]
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

    def view2D(self):
        glClear(GL_COLOR_BUFFER_BIT)

        # ViewPort esquerda
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, 800, 650)
        glColor3f(0, 1, 0)
        glRotatef(90, 0, 0, 1)
        self.desenha_objeto()

        # ViewPort Direita inferior
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(800, 0, 480, 325)
        glColor3f(0, 0, 1)
        self.desenha_objeto()

        # ViewPort Direita superior
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(800, 325, 480, 325)
        glColor3f(0, 0, 1)

        self.desenha_objeto()
        glFlush()


if __name__ == '__main__':
    Main()
