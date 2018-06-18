# -*- coding: utf-8 -*-
import sys
from objloader import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from pygame import *
import graphics
import math


class Viewport:
    def __init__(self):
        self.height = 0
        self.width = 0
        self.eye = {"x": 0, "y": 0, "z": 0}
        self.look = {"x": 0, "y": 0, "z": 0}
        self.up = {"x": 0, "y": 0, "z": 0}
        self.aspect = None
        self.startx = None
        self.starty = None

    def init(self, ox, oy, w, h):
        self.startx = ox
        self.starty = oy
        self.width = w
        self.height = h
        self.aspect = self.width / self.height

    def lookAt(self, e, l, u):
        self.eye = e
        self.look = l
        self.up = u
        self.set()

    def set(self):
        glViewport(self.startx, self.starty, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, self.aspect, 0.01, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye["x"], self.eye["y"], self.eye["z"],
                  self.look["x"], self.look["y"], self.look["z"],
                  self.up["x"], self.up["y"], self.up["z"])


class Main:
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    angleY = 0
    angleX = 0
    cube_angle = 0
    eixoY = 10
    eixoX = 0

    sol_ang = 0
    width = 1280
    height = 650

    front = Viewport()
    top = Viewport()
    side = Viewport()

    # camera = Viewport()

    def __init__(self):
        pygame.init()
        self.viewport = (self.width, self.height)
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
        self.coordinates = [0, 0, 0]

        self.init()

        self.pokebola = OBJ("pokebola.obj", swapyz=True)

        # renderiza objeto sem textura
        self.ground = graphics.ObjLoader("plane.obj")

        # importa uma imagem para agir como textura do objeto
        self.ground_texture = graphics.load_texture("plane.png")

        self.loop()

    def loop(self):
        clock = pygame.time.Clock()
        done = False
        self.sol_ang += .5
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
                    pass

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
        # VIEWPORT GRANDE DA ESQUERDA
        self.front.init(0, 0, 800, 650)
        self.front.lookAt({"x": 0, "y": 0, "z": 30},
                          {"x": 0, "y": 0, "z": 0},
                          {"x": 0, "y": 1, "z": 0})

        # VIEWPORT DO CANTO INFERIOR DIREITO
        self.top.init(800, 0, 480, 325)
        self.top.lookAt({"x": 0, "y": 30, "z": 0},
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 0, "y": 0, "z": -1})

        # VIEWPORT DO CANTO SUPERIOR DIREITO
        self.side.init(800, 325, 480, 325)
        self.side.lookAt({"x": 30, "y": 0, "z": 0},
                         {"x": 0, "y": 0, "z": 0},
                         {"x": 0, "y": 1, "z": 0})

        # self.camera.init(width / 2, height / 2, width / 2, height / 2)
        # self.camera.lookAt({"x": 30, "y": 30, "z": 30},
        #                    {"x": 0, "y": 0, "z": 0},
        #                    {"x": -0.577, "y": 0.577, "z": -0.577})

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
        glColor3f(1, 0, 0)

        glPopMatrix()

    def objects(self):
        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])

        glPushMatrix()

        # faz a pokebola ficar girando
        glRotatef(self.cube_angle, 0, 1, 0)
        glRotatef(45, 1, 0, 0)
        glTranslatef(0, 0, -1)
        glCallList(self.pokebola.gl_list)

        glPopMatrix()
        glPushMatrix()
        # renderiza o chao
        glColor3f(0, 23, 1)
        glRotatef(1, 1, 0, 0)
        glTranslatef(0, -1.5, 0)
        self.ground.render_texture(self.ground_texture, ((0, 0), (2, 0), (2, 2), (0, 2)))
        glPopMatrix()

        self.sol()
        self.lua()
        self.plano()

    def lua(self):
        glPushMatrix()

        glRotatef(self.sol_ang, 0, 0, -1)

        glTranslatef(-15, 0, 0)

        # faz a pokebola ficar girando
        glRotatef(self.cube_angle, 0, 1, 0)
        glTranslatef(0, 0, -1)

        glCallList(self.pokebola.gl_list)

        glPopMatrix()

    def sol(self):
        # glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])
        glPushMatrix()

        glRotatef(self.sol_ang, 0, 0, -1)

        glTranslatef(15, 0, 0)

        # faz a pokebola ficar girando
        glRotatef(self.cube_angle, 0, 1, 0)
        glTranslatef(0, 0, -1)

        glCallList(self.pokebola.gl_list)

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
        glLightfv(GL_LIGHT0, GL_AMBIENT, luzAmbiente)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, luzDifusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, luzEspecular)
        glLightfv(GL_LIGHT0, GL_POSITION, posicaoLuz)

        # Add positioned light:
        # glLightfv(GL_LIGHT1, GL_SPECULAR, (0.9, 0.9, 0.9, 0.8))
        # glLightfv(GL_LIGHT1, GL_AMBIENT, (0.65, 0.65, 0.65, 0.9))
        # glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.65, 0.65, 0.65, 0.9))
        # glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 0.2))
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 0.9))

        # gluLookAt(camera.x, camera.y, camera.z,  lookat.x, lookat.y, lookat.z, 0, 1, 0)
        self.front.set()
        self.objects()
        # self.lua()
        # self.sol()

        self.top.set()
        self.objects()

        self.side.set()
        self.objects()

        # self.camera.set()
        # self.objects()


if __name__ == '__main__':
    Main()
