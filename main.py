import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame and OpenGL
def init_pygame_opengl():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)  # Adjusted FOV angle and aspect ratio
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    return display

# Define object classes
class Cube:
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

    def __init__(self, position):
        self.position = position

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        for i, surface in enumerate(self.surfaces):
            glColor3fv(self.colors[i])
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glBegin(GL_LINES)
        glColor3f(0, 0, 0)  # Black for edges
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()
        glPopMatrix()

class Compass:
    @staticmethod
    def draw(yaw, pitch):
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

class Ground:
    @staticmethod
    def draw():
        glBegin(GL_LINES)
        glColor3f(0.5, 0.5, 0.5)
        for i in range(-50, 51):
            glVertex3f(i, -1, -50)
            glVertex3f(i, -1, 50)
            glVertex3f(-50, -1, i)
            glVertex3f(50, -1, i)
        glEnd()

def draw_text(position, text_string):
    font = pygame.font.SysFont("Arial", 18)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def main():
    display = init_pygame_opengl()

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
        pitch += mouse_movement[1] * mouse_sensitivity  # Inverted pitch correction

        # Clamp pitch to prevent looking beyond straight up and straight down
        pitch = max(-90, min(90, pitch))

        # Clear screen and reset view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(x, y, z, x + math.sin(math.radians(yaw)), y + math.sin(math.radians(pitch)), z + math.cos(math.radians(yaw)), 0, 1, 0)

        # Draw ground
        Ground.draw()

        # Draw objects
        for obj in objects:
            obj.draw()

        # Draw compass
        Compass.draw(yaw, pitch)

        # Switch to orthographic projection to draw text
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, display[0], 0, display[1])
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw camera position
        draw_text((10, 10), f"Position: ({x:.2f}, {y:.2f}, {z:.2f})")

        # Restore perspective projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
