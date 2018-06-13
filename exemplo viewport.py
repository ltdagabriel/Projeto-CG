from objloader import *

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


class Main:
    def __init__(self):
        self.cont = 0
        glutInit(len(sys.argv), sys.argv)

        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

        # posicao inicial da janela no computador (nao tem nada a ver com o que tem dentro)
        glutInitWindowPosition(50, 0)
        glutInitWindowSize(1280, 650)
        glutCreateWindow("PROJETO CGR")

        self.init()

        self.pokebola = OBJ("pokebola.obj", swapyz=True)

        glutDisplayFunc(self.display)
        glutMainLoop()

    def teapot(self):
        glRotatef(45, 1, 0, 0)
        glRotatef(self.cont, 0, 0, 1)
        glutWireTeapot(1)

        self.cont = 0 if self.cont == 360 else self.cont + 1

        glutPostRedisplay()

    def init(self):
        # Reinicializa a cor de fundo
        glClearColor(1, 1, 1, 1)

        glMatrixMode(GL_PROJECTION)
        # Matriz de identidade
        glLoadIdentity()

        gluOrtho2D(-100, 100, -100, 100)

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

        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(0, 0, 800, 650)
        glColor3f(0, 1, 0)
        glRotatef(90, 0, 0, 1)
        self.desenha_objeto()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(800, 0, 480, 325)
        glColor3f(0, 0, 1)
        self.desenha_objeto()

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glViewport(800, 325, 480, 325)
        glColor3f(0, 0, 1)
        self.desenha_objeto()
        glFlush()



if __name__ == '__main__':
    Main()
