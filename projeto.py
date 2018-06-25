# -*- coding: utf-8 -*-
# autores:
#   - Gabriel Choptian
#   - Caio Cesar Hideo Nakai
#   - Rafael Menezes Barboza

# Projeto OPENGL
# Controle: UP/DOWN - scale up/down
#           LEFT/RIGHT - rotate left/right
#           F1 - Toggle surface as SMOOTH or FLAT

# Python imports
from math import *

# OpenGL imports for python
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print "OpenGL wrapper for python not found"

try:
    # Utilizado para importar objetos com MTL
    from ObjectLoaders.objloader import *

    # Utilizado para importar Objeto sem textura e adicionar textura externamente
    from ObjectLoaders import graphics
except:
    print "Não foi encontrado as bibliotecas da pasta ObjectLoaders"

# Last time when sphere was re-displayed
last_time = 0


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


class Projeto:
    eixo_angle = 0
    sol_ang = 0
    sol_raio = 30

    # Constructor for the sphere class
    def __init__(self):

        self.user_theta = 0
        self.user_height = 0

        # Direction of light
        self.sol_position = [0.0, 0, -1, 0]
        self.lua_position = [0.0, 0, -1, 0]

        # Intensity of light
        self.sol_intensity = [0.7, 0.5, 0.5, 1.0]
        self.lua_intensity = [0.3, 0.3, 0.7, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.2, 0.2, 0.2, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

        # Declaração de viewport
        self.front = Viewport()
        self.top = Viewport()
        self.side = Viewport()

        # Camera
        self.cameraPos = {'x': 0, 'y': 0, 'z': 30}
        self.cameraFront = {'x': 0, 'y': 0, 'z': -1}
        self.cameraUp = {'x': 0, 'y': 1, 'z': 0}

        # Carrega Objetos
        self.pokebola = OBJ("pokebola.obj", swapyz=True)

        self.matinho = OBJ("matinho.obj", swapyz=True)

        self.pikachu = OBJ("pikachu.obj", swapyz=True)

        self.arvorinha = OBJ("Lowpoly_tree_sample.obj", swapyz=True)

        self.luazinha = OBJ("Moon.obj", swapyz=True)

        self.solzinho = OBJ("Sun.obj", swapyz=True)

        # renderiza objeto sem textura
        self.ground = graphics.ObjLoader("plane.obj")

        # importa uma imagem para agir como textura do objeto
        self.ground_texture = graphics.load_texture("plane.png")

    def lighting(self):

        # Set position and intensity of light

        # SOL
        glLightfv(GL_LIGHT0, GL_POSITION, self.sol_position)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.sol_intensity)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.sol_intensity)

        # LUA
        glLightfv(GL_LIGHT1, GL_POSITION, self.lua_position)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, self.lua_intensity)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.lua_intensity)

        glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

    # Initialize
    def init(self):

        # Set background color to black
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        # Set OpenGL parameters
        glEnable(GL_DEPTH_TEST)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Compute location
    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)

        # Set matrix mode
        glMatrixMode(GL_PROJECTION)

        # Reset matrix
        glLoadIdentity()

        # VIEWPORT GRANDE DA ESQUERDA
        self.front.init(0, 0, 800, 650)
        self.front.lookAt(self.cameraPos,
                          {"x": self.cameraPos['x'] + self.cameraFront['x'],
                           "y": self.cameraPos['y'] + self.cameraFront['y'],
                           "z": self.cameraPos['z'] + self.cameraFront['z']},
                          self.cameraUp)

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

    def display(self):

        self.lighting()

        # atualiza o angulos
        self.eixo_angle = 0 if self.eixo_angle >= 360 else self.eixo_angle + 1
        self.sol_ang += .005

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set color to white
        glColor3f(1.0, 1.0, 1.0)

        # Set shade model
        glShadeModel(self.surface)

        self.front.set()
        self.objects()

        self.top.set()
        self.objects()

        self.side.set()
        self.objects()

        glutSwapBuffers()

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
        glPushMatrix()

        # faz a pokebola ficar girando
        glTranslatef(0, 8, 0)

        glRotatef(self.eixo_angle, 0, 1, 0)

        glRotatef(45, 1, 0, 0)
        glScalef(1.5, 1.5, 1.5)
        glTranslatef(0, 0, -1)
        glCallList(self.pokebola.gl_list)

        glPopMatrix()

        glPushMatrix()
        glRotatef(90, -1, 0, 0)
        glRotatef(180, 0, 0, 1)
        glTranslatef(0, 0, -1)
        glColor3f(1, 1, 0)
        glCallList(self.pikachu.gl_list)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(2, -1, -10)
        glRotatef(90, -1, 0, 0)
        glScalef(0.5, 0.5, 0.5)
        glCallList(self.arvorinha.gl_list)
        glPopMatrix()

        glPushMatrix()
        # renderiza o chao
        glColor3f(0, 23, 1)
        glRotatef(1, 1, 0, 0)
        glTranslatef(0, -2, 0)
        glScalef(10, 10, 10)
        # glCallList(self.matinho.gl_list)
        self.ground.render_texture(self.ground_texture, ((0, 0), (2, 0), (2, 2), (0, 2)))
        glPopMatrix()

        self.sol()
        self.plano()
        self.lua()

    def lua(self):

        self.lua_position = [-self.sol_raio * cos(self.sol_ang), -self.sol_raio * sin(self.sol_ang), 0, 1]
        glPushMatrix()

        glRotatef(self.sol_ang, 0, 0, -1)

        glTranslatef(-1 * self.sol_raio * cos(self.sol_ang), -1 * self.sol_raio * sin(self.sol_ang), 0)
        glTranslatef(0, 0, -5)
        glColor3f(196, 196, 196)
        # faz a pokebola ficar girando
        glScalef(0.1, 0.1, 0.1)

        glCallList(self.luazinha.gl_list)

        glPopMatrix()

    def sol(self):
        self.sol_position = [self.sol_raio * cos(self.sol_ang), self.sol_raio * sin(self.sol_ang), 0, 1]

        glPushMatrix()

        glTranslatef(self.sol_raio * cos(self.sol_ang), self.sol_raio * sin(self.sol_ang), 0)

        glRotatef(self.eixo_angle, 0, 1, 0)
        glTranslatef(0, 0, -5)
        glColor3f(253, 184, 19)
        glScalef(0.1, 0.1, 0.1)
        # faz a pokebola ficar girando

        glCallList(self.solzinho.gl_list)

        glPopMatrix()

    # Keyboard controller for sphere
    def special(self, key, x, y):
        # Scale the sphere up or down
        if key == GLUT_KEY_UP:
            self.cameraPos['z'] -= 0.1

        if key == GLUT_KEY_DOWN:
            self.cameraPos['z'] += 0.1

            # Rotate the cube
        if key == GLUT_KEY_LEFT:
            self.cameraPos['x'] -= 0.1
        if key == GLUT_KEY_RIGHT:
            self.cameraPos['x'] += 0.1

        # Toggle the surface
        if key == GLUT_KEY_F1:
            self.surface = GL_FLAT if GL_SMOOTH else GL_SMOOTH

        self.compute_location()
        glutPostRedisplay()

    # The idle callback
    def idle(self):
        global last_time
        time = glutGet(GLUT_ELAPSED_TIME)

        if last_time == 0 or time >= last_time + 40:
            last_time = time
            glutPostRedisplay()

    # The visibility callback
    def visible(self, vis):
        if vis == GLUT_VISIBLE:
            glutIdleFunc(self.idle)
        else:
            glutIdleFunc(None)


# The main function
def main():
    # Initialize the OpenGL pipeline
    glutInit(sys.argv)

    # Set OpenGL display mode
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)

    # Set the Window size and position
    glutInitWindowSize(1280, 650)
    glutInitWindowPosition(50, 50)

    # Create the window with given title
    glutCreateWindow('PROJETO CGR')

    # Instantiate the sphere object
    s = Projeto()

    s.init()

    # Set the callback function for display
    glutDisplayFunc(s.display)

    # Set the callback function for the visibility
    glutVisibilityFunc(s.visible)

    # Set the callback for special function
    glutSpecialFunc(s.special)

    # Run the OpenGL main loop
    glutMainLoop()


# Call the main function
if __name__ == '__main__':
    main()
