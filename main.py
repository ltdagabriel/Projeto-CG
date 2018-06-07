# -*- coding: utf-8 -*-
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from objloader import *
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import graphics


class Cube(object):
    left_key = False
    right_key = False
    up_key = False
    down_key = False
    angle = 0
    cube_angle = 0

    # -------------------------------------
    def __init__(self, viewport):
        self.vertices = []
        self.faces = []

        # inicializa a camera
        # ---Coordinates----[x,y,z]-----------------------------
        self.coordinates = [0, 0, 0]

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = viewport
        gluPerspective(90.0, width / float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

        # renderiza objeto sem textura
        self.ground = graphics.ObjLoader("plane.obj")

        # importa uma imagem para agir como textura do objeto
        self.ground_texture = graphics.load_texture("plane.png")

        # renderiza objeto com arquivo MTL
        self.obj = OBJ("pokebola.obj", swapyz=True)

    def render_scene(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glClearColor(0.7,0.9,1,1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Add positioned light:
        glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))

        glTranslatef(0, -0.5, 0)

        gluLookAt(0, 0, 0, math.sin(math.radians(self.angle)), 0, math.cos(math.radians(self.angle)) * -1, 0, 1, 0)

        glTranslatef(self.coordinates[0], self.coordinates[1], self.coordinates[2])

        # renderiza o chao
        self.ground.render_texture(self.ground_texture, ((0, 0), (2, 0), (2, 2), (0, 2)))

        # coloca a pokebola acima do chao
        glTranslatef(-7.5, 2, 0)

        # faz a pokebola ficar girando
        glRotatef(self.cube_angle, 0, 1, 0)
        glRotatef(45, 1, 0, 0)

        # renderiza a pokebola
        glCallList(self.obj.gl_list)

    # glTranslatef(-7.5,2,0)
    # glRotatef(self.cube_angle,0,1,0)
    # glRotatef(45,1,0,0)
    # self.cube.render_texture(self.rubik_id,((0,0),(1,0),(1,1),(0,1)))
    # self.pokemon.render_scene()

    # self.monkey.render_scene()

    def move_forward(self):
        self.coordinates[2] += 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[0] -= 0.1 * math.sin(math.radians(self.angle))

    def move_back(self):
        self.coordinates[2] -= 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[0] += 0.1 * math.sin(math.radians(self.angle))

    def move_left(self):
        self.coordinates[0] += 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[2] += 0.1 * math.sin(math.radians(self.angle))

    def move_right(self):
        self.coordinates[0] -= 0.1 * math.cos(math.radians(self.angle))
        self.coordinates[2] -= 0.1 * math.sin(math.radians(self.angle))

    def rotate(self, n):
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
        self.angle += n

    def update(self):
        if self.left_key:
            self.move_left()
        elif self.right_key:
            self.move_right()
        elif self.up_key:
            self.move_forward()
        elif self.down_key:
            self.move_back()

        pos = pygame.mouse.get_pos()
        if pos[0] < 75:
            self.rotate(-1.2)
        elif pos[0] > 565:
            self.rotate(1.2)

        if self.cube_angle >= 360:
            self.cube_angle = 0
        else:
            self.cube_angle += 0.5

    def keyup(self):
        self.left_key = False
        self.right_key = False
        self.up_key = False
        self.down_key = False

    def delete_texture(self):
        pass

# glDeleteTextures(self.rubik_id)
# glDeleteTextures(self.surface_id)


def main():
    pygame.init()
    viewport = (800, 600)
    pygame.display.set_mode(viewport, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Projeto OpenGL")
    clock = pygame.time.Clock()
    done = False

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # iluminação
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)

    # ativa textuta de arquivos mtl
    glEnable(GL_COLOR_MATERIAL)
    # ativa sombra de arquivos obj
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    cube = Cube(viewport)

    # ----------- Main Program Loop -------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    cube.move_left()
                    cube.left_key = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    cube.move_right()
                    cube.right_key = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    cube.move_forward()
                    cube.up_key = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    cube.move_back()
                    cube.down_key = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    cube.keyup()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    cube.keyup()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    cube.keyup()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    cube.keyup()

        cube.update()
        cube.render_scene()

        pygame.display.flip()
        clock.tick(30)

    cube.delete_texture()
    pygame.quit()


if __name__ == '__main__':
    main()
