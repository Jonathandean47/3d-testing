import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys
import numpy

debug = True

# Define object classes
class Cube:
    def __init__(self, position, size = 1):
        self.position = position
        self.size = size
        self.vertices = (
            (size, -size, -size),
            (size, size, -size),
            (-size, size, -size),
            (-size, -size, -size),
            (size, -size, size),
            (size, size, size),
            (-size, -size, size),
            (-size, size, size)
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
    
    def get_bounding_box(self):
        min_x = self.position[0] - self.size
        max_x = self.position[0] + self.size
        min_y = self.position[1] - self.size
        max_y = self.position[1] + self.size
        min_z = self.position[2] - self.size
        max_z = self.position[2] + self.size
        return (min_x, max_x, min_y, max_y, min_z, max_z)
    
    def get_surface_normal(self, surface_index):
        surface = self.surfaces[surface_index]
        v1 = self.vertices[surface[1]]
        v2 = self.vertices[surface[0]]
        v3 = self.vertices[surface[2]]
        normal = numpy.cross(numpy.subtract(v2, v1), numpy.subtract(v3, v1))
        normal = normal / numpy.linalg.norm(normal)
        return normal
    
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

class Player:
    def __init__(self, position=(0, 0.25, 5), speed=0.1, gravity=-0.01, jump_velocity=0.2):
        self.position = list(position)
        self.speed = speed
        self.gravity = gravity
        self.vertical_velocity = 0
        self.jump_velocity = jump_velocity
        self.yaw = 0
        self.pitch = 0
        self.mouse_sensitivity = 0.1
        self.radius = 0.1
        self.height = 0.5

    def move(self, keys):
        x, y, z = self.position
        if keys[K_w]:
            x -= math.sin(math.radians(self.yaw)) * self.speed
            z -= math.cos(math.radians(self.yaw)) * self.speed
        if keys[K_s]:
            x += math.sin(math.radians(self.yaw)) * self.speed
            z += math.cos(math.radians(self.yaw)) * self.speed
        if keys[K_a]:
            x += math.sin(math.radians(self.yaw + 90)) * self.speed
            z += math.cos(math.radians(self.yaw + 90)) * self.speed
        if keys[K_d]:
            x += math.sin(math.radians(self.yaw - 90)) * self.speed
            z += math.cos(math.radians(self.yaw - 90)) * self.speed
        if keys[K_SPACE] and (y == 0 or debug):  # Allow jumping only if on the ground
            self.vertical_velocity = self.jump_velocity
        # if keys[K_c]:
        #     y -= self.speed
        
        self.position = [x, y, z]

    def apply_gravity(self):
        self.vertical_velocity += self.gravity
        self.position[1] += self.vertical_velocity

        # Check for collision with the ground
        if self.position[1] < 0:  # Assuming the ground is at y = -1
            self.position[1] = 0
            self.vertical_velocity = 0  # Reset velocity when hitting the ground

    def update_view(self):
        mouse_movement = pygame.mouse.get_rel()
        self.yaw += mouse_movement[0] * self.mouse_sensitivity
        self.pitch += mouse_movement[1] * self.mouse_sensitivity  # Inverted pitch correction

        # Clamp pitch to prevent looking beyond straight up and straight down
        self.pitch = max(-90, min(90, self.pitch))

        # Bound yaw to -180 to 180 degrees
        self.yaw = (self.yaw + 180) % 360 - 180

    def get_view_matrix(self):
        x, y, z = self.position
        return (x, y, z, x + math.sin(math.radians(self.yaw)), y + math.sin(math.radians(self.pitch)), z + math.cos(math.radians(self.yaw)), 0, 1, 0)
    
    def get_bounding_box(self):
        min_x = self.position[0] - self.radius
        max_x = self.position[0] + self.radius
        min_y = self.position[1] - self.height / 2
        max_y = self.position[1] + self.height / 2
        min_z = self.position[2] - self.radius
        max_z = self.position[2] + self.radius
        return (min_x, max_x, min_y, max_y, min_z, max_z)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1], self.position[2])
        glRotatef(-90, 1, 0, 0)  # Rotate cylinder to be vertical
        quadric = gluNewQuadric()
        glColor3f(1, 0, 0)  # Red color for the player

        # Draw cylinder body
        gluCylinder(quadric, self.radius, self.radius, self.height, 32, 32)

        # Draw top cap
        glPushMatrix()
        glTranslatef(0, 0, self.height)
        glColor3f(0, 0, 1)
        gluDisk(quadric, 0, self.radius, 32, 1)
        glPopMatrix()

        # Draw bottom cap
        glPushMatrix()
        glColor3f(0, 1, 1)
        gluDisk(quadric, 0, self.radius, 32, 1)
        glPopMatrix()

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
        for i in range(-10, 11):
            glVertex3f(i, 0, -50)
            glVertex3f(i, 0, 50)
            glVertex3f(-50, 0, i)
            glVertex3f(50, 0, i)
        glEnd()

# Initialize Pygame and OpenGL
def init_pygame_opengl():
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(72, (display[0] / display[1]), 0.001, 5000.0)  # Adjusted FOV angle and aspect ratio
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    return display

def draw_text(position, text_string):
    font = pygame.font.SysFont("Arial", 18)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
def check_collision(bounding_box1, bounding_box2):
    min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = bounding_box1
    min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = bounding_box2

    if (max_x1 >= min_x2 and min_x1 <= max_x2 and
        max_y1 >= min_y2 and min_y1 <= max_y2 and
        max_z1 >= min_z2 and min_z1 <= max_z2):
        return True
    return False

def reflect_vector(vector, normal):
    return vector - 2 * numpy.dot(vector, normal) * normal

def main():
    display = init_pygame_opengl()
    clock = pygame.time.Clock()

    # Create player
    player = Player()
    
    # Create objects
    objects = [
        Cube((0, 1, 0), size = 1),
        Cube((3, 0, 0), size = 2),
        Cube((-2, 0, 0), size = 0.5)
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        player.apply_gravity()
        player.update_view()
        
        # Check for collisions and adjust camera position
        player_bounding_box = player.get_bounding_box()
        for obj in objects:
            obj_bounding_box = obj.get_bounding_box()
            if check_collision(player_bounding_box, obj_bounding_box):
                # Calculate the normal vector of the collision surface
                for i, surface in enumerate(obj.surfaces):
                    if check_collision(player_bounding_box, obj.get_bounding_box()):
                        normal = obj.get_surface_normal(i)
                        break

                # Calculate the reflection vector
                movement_vector = numpy.array([math.sin(math.radians(player.yaw)) * player.speed, 0, math.cos(math.radians(player.yaw)) * player.speed])
                reflection_vector = reflect_vector(movement_vector, normal)

                # Adjust the player's position
                player.position[0] += reflection_vector[0]
                player.position[2] += reflection_vector[2]

                # Adjust the player's vertical position if necessary
                if player.position[1] < obj_bounding_box[3] + player.height / 2 and \
                    player.position[0] > obj_bounding_box[0] and player.position[0] < obj_bounding_box[1] and \
                    player.position[2] > obj_bounding_box[4] and player.position[2] < obj_bounding_box[5]:
                    player.position[1] = obj_bounding_box[3] + player.height / 2
                    player.vertical_velocity = 0  # Reset velocity when landing on top


        # Clear screen and reset view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(*player.get_view_matrix())

        # Draw ground
        Ground.draw()
        
        # Draw objects
        for obj in objects:
            obj.draw()

        # Draw player
        player.draw()
        
        if debug:
            # Draw compass
            Compass.draw(player.yaw, player.pitch)

            # Switch to orthographic projection to draw text
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, display[0], 0, display[1])
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            # Draw camera position
            draw_text((10, 10), f"({player.position[0]:.2f}, {player.position[1]:.2f}, {player.position[2]:.2f})")
            draw_text((display[0]-180, 10), f"({player.yaw:.2f}°, {-player.pitch:.2f}°)")

            # Restore perspective projection
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
    sys.exit()
