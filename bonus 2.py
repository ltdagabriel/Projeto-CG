from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


class Main:
    def __init__(self):
        self.cont = 0
        glutInit(len(sys.argv), sys.argv)

        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
        glutInitWindowPosition(200, 0)
        glutInitWindowSize(800, 800)
        glutCreateWindow("Bonus 2 em python by: Gabriel")

        self.init()

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

        # habilita profundidade
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_MODELVIEW)

        # Matriz de identidade
        glLoadIdentity()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        pontos = [[0, 400], [400, 400], [400, 400]]
        # INIT ViewPort 1 - Canto Superior Esquerdo

        glViewport(pontos[0][0], pontos[0][1], pontos[1][0], pontos[1][1])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Projecao ortogonal
        glOrtho(-2, 2, -2, 2, 1, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Camera
        gluLookAt(0, 1, 0, 0, 0, 0, 0, 0, 1)

        # Color RED
        glColor3f(1, 0, 0)

        glutWireTeapot(1)
        # END ViewPort 1
        # -------------------------------------------------------
        # INIT ViewPort 2 - Canto Superior Direito
        glViewport(pontos[1][0], pontos[1][1], pontos[2][0], pontos[2][1])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Projecao ortogonal
        glOrtho(-2, 2, -2, 2, 1, 50)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Camera
        gluLookAt(1, 0, 0, 0, 0, 0, 0, 1, 0)

        # Color RED
        glColor3f(1, 0, 0)

        glutWireTeapot(1)
        # END ViewPort 2
        # -------------------------------------------------------
        pontos = [[0, 0], [400, 400], [400, 0]]
        # INIT ViewPort 3 - Canto Inferior Esquerdo
        glViewport(pontos[0][0], pontos[0][1], pontos[1][0], pontos[1][1])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Projecao ortogonal
        glOrtho(-2.0, 2.0, -2.0, 2.0, 1.0, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Camera
        gluLookAt(0, 0, 1, 0, 0, 0, 0, 1, 0)

        # Color RED
        glColor3f(1, 0, 0)

        glutWireTeapot(1)
        # END ViewPort 3
        # -------------------------------------------------------
        # INIT ViewPort 4 - Canto Inferior Direito
        glViewport(pontos[2][0], pontos[2][1], pontos[1][0], pontos[1][1])

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Projecao ortogonal
        gluPerspective(70.0, 1.0, 1.0, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Camera
        gluLookAt(0, 0, 3, 0, 0, 0, 0, 1, 0)

        # Color RED
        glColor3f(1, 0, 0)

        self.teapot()
        # END ViewPort 4

        glFlush()


if __name__ == '__main__':
    Main()
