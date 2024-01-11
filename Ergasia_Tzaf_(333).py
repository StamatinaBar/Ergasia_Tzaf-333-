from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
from OpenGL.GLUT import glutSolidCube, glutInit

##Falling Sphere attributes###
class Sphere:
    def __init__(self):
        self.position = [-4.0, -1.0, 10.0]  # Initial position of the falling sphere
        self.velocity = [0.0, 0.0, 0.0]      # Initial velocity of the falling sphere

    def update(self):
        global gravity, bounce_factor
        self.velocity[2] += gravity        # Apply gravity to the vertical velocity
        self.position[2] += self.velocity[2]  # Update the vertical position based on velocity

        if self.position[2] < 1.0:
            self.position[2] = 1.0           # Ensure the sphere stays above the ground
            self.velocity[2] = -self.velocity[2] * bounce_factor  # Apply bounce

gravity = -0.05        # Gravity affecting the falling sphere
bounce_factor = 0.7    # Factor determining the bounce after hitting the ground

falling_sphere = Sphere()
falling_sphere_active = False

pygame.init()
glutInit()
display = (400, 300)
screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# OpenGL setup
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glShadeModel(GL_SMOOTH)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])

sphere = gluNewQuadric()

# Perspective projection
glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

# Set up the initial modelview matrix
glMatrixMode(GL_MODELVIEW)
gluLookAt(0, -8, 0, 0, 0, 0, 0, 0, 1)
viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
glLoadIdentity()

# Initialize mouse movement and center mouse on screen
displayCenter = [screen.get_size()[i] // 2 for i in range(2)]
mouseMove = [0, 0]
pygame.mouse.set_pos(displayCenter)

up_down_angle = 0.0
paused = False
wireframe_mode = False  # Track wireframe mode
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                run = False
            if event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                paused = not paused
                pygame.mouse.set_pos(displayCenter)
            if event.key == pygame.K_1:  # Toggle wireframe mode on "1" key
                wireframe_mode = not wireframe_mode
                if wireframe_mode:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                else:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            if event.key == pygame.K_2:
                falling_sphere_active = True  # Activate falling sphere on "2" key

        if not paused:
            if event.type == pygame.MOUSEMOTION:
                mouseMove = [event.pos[i] - displayCenter[i] for i in range(2)]
            pygame.mouse.set_pos(displayCenter)

    if falling_sphere_active:
        falling_sphere.update()

    if not paused:
        #### Mouse view process ###
        # Get keys
        keypress = pygame.key.get_pressed()

        # Init model view matrix
        glLoadIdentity()

        # Apply the look up and down
        up_down_angle += mouseMove[1] * 0.1
        glRotatef(up_down_angle, 1.0, 0.0, 0.0)

        # Init the view matrix
        glPushMatrix()
        glLoadIdentity()

        # Apply the movement
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, 0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1, 0, 0)

        # Left and right rotation og the mouse
        glRotatef(mouseMove[0] * 0.1, 0.0, 1.0, 0.0)

        ##Matrix represents the camera's position and orientation
        # Multiply the current matrix to get the new view matrix and store the final view matrix
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # Apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)

        glLightfv(GL_LIGHT0, GL_POSITION, [1, -1, 1, 0])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        # Ground plane
        glColor4f(0.5, 0.5, 0.5, 1)
        glBegin(GL_QUADS)
        glVertex3f(-10, -10, -2)
        glVertex3f(10, -10, -2)
        glVertex3f(10, 10, -2)
        glVertex3f(-10, 10, -2)
        glEnd()

        # Sphere creation
        glTranslatef(-1.5, 0, 0)   #position in the 3D space (x,y,z)
        glColor4f(0.5, 0.2, 0.2, 1)  #colour
        gluSphere(sphere, 1.0, 32, 16)

        # Cylinder creation
        glTranslatef(3, 0, -1)
        glColor4f(0.2, 0.2, 0.5, 1)
        gluCylinder(sphere, 1.0, 1.0, 2.0, 32, 16)

        # Cube creation
        glTranslatef(3, 0, -1)
        glColor4f(0.3, 0.2, 0.5, 1)
        glutSolidCube(2.0)

        # Falling sphere
        glTranslatef(*falling_sphere.position)
        glColor3f(1.0, 0.0, 0.0)
        gluSphere(sphere, 1.0, 32, 16)

        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

pygame.quit()
