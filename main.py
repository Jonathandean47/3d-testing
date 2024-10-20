import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame and OpenGL
pygame.init()
info = pygame.display.Info()
display = (1200, 900)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(60, (display[0] / display[1]), 0.1, 1000.0)  # Adjusted FOV angle and aspect ratio

# Define object classes
class Cube:
    def __init__(self, position):
        self.position = position

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            glColor3fv(colors[i])
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)  # Black for edges
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()
        glPopMatrix()

# Define vertices, surfaces, and edges for a cube
vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
)

surfaces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)

colors = (
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
)

# Create objects
objects = [
    Cube((0, 1, 0)),
    Cube((2, 0, 0)),
    Cube((-2, 0, 0))
]

# Player movement variables
x, y, z = 0, 0, 0
yaw, pitch = 0, 0
speed = 0.1
mouse_sensitivity = 0.1

# Hide the mouse cursor and center it
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

def draw_compass(yaw, pitch):
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.8, -0.8, -1)  # Position the compass in the corner
    glRotatef(yaw, 0, 1, 0)  # Rotate based on yaw
    glRotatef(pitch, 1, 0, 0)  # Rotate based on pitch

    # Draw compass
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)  # Red for North
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, -0.1)
    glColor3f(0, 1, 0)  # Green for East
    glVertex3f(0, 0, 0)
    glVertex3f(0.1, 0, 0)
    glColor3f(0, 0, 1)  # Blue for South
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 0.1)
    glColor3f(1, 1, 0)  # Yellow for West
    glVertex3f(0, 0, 0)
    glVertex3f(-0.1, 0, 0)
    glColor3f(1, 1, 1)  # White for Up/Down
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0.1, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -0.1, 0)
    glEnd()

    glPopMatrix()

def draw_ground():
    glBegin(GL_LINES)
    glColor3f(0.5, 0.5, 0.5)
    for i in range(-50, 51):
        glVertex3f(i, -1, -50)
        glVertex3f(i, -1, 50)
        glVertex3f(-50, -1, i)
        glVertex3f(50, -1, i)
    glEnd()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    if keys[K_w]:
        x -= math.sin(math.radians(yaw)) * speed
        z -= math.cos(math.radians(yaw)) * speed
    if keys[K_s]:
        x += math.sin(math.radians(yaw)) * speed
        z += math.cos(math.radians(yaw)) * speed
    if keys[K_a]:
        x += math.sin(math.radians(yaw + 90)) * speed
        z += math.cos(math.radians(yaw + 90)) * speed
    if keys[K_d]:
        x += math.sin(math.radians(yaw - 90)) * speed
        z += math.cos(math.radians(yaw - 90)) * speed
    if keys[K_SPACE]:
        y += speed
    if keys[K_c]:
        y -= speed

    # Mouse movement
    mouse_movement = pygame.mouse.get_rel()
    yaw += mouse_movement[0] * mouse_sensitivity
    pitch -= mouse_movement[1] * mouse_sensitivity  # Inverted pitch correction

    # Clear screen and reset view
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(x, y, z, x + math.sin(math.radians(yaw)), y + math.sin(math.radians(pitch)), z + math.cos(math.radians(yaw)), 0, 1, 0)

    # Draw ground
    draw_ground()

    # Draw objects
    for obj in objects:
        obj.draw()

    # Draw compass
    draw_compass(yaw, pitch)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
