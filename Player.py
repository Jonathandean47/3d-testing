import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import config

class Player:
    def __init__(self, position=(0, 0.5, 5), speed=0.1, gravity=-0.01, jump_velocity=0.2):
        self.position = list(position)
        self.velocity = [0, 0, 0]  # Horizontal velocity vector
        self.speed = speed
        self.gravity = gravity
        self.vertical_velocity = 0  # Vertical velocity
        self.jump_velocity = jump_velocity
        self.yaw = 0
        self.pitch = 0
        self.mouse_sensitivity = 0.1
        self.radius = 0.1
        self.height = 0.5

    def move(self, keys):
        acceleration = self.speed
        if keys[K_w]:
            self.velocity[0] -= math.sin(math.radians(self.yaw)) * acceleration
            self.velocity[2] -= math.cos(math.radians(self.yaw)) * acceleration
        if keys[K_s]:
            self.velocity[0] += math.sin(math.radians(self.yaw)) * acceleration
            self.velocity[2] += math.cos(math.radians(self.yaw)) * acceleration
        if keys[K_a]:
            self.velocity[0] += math.sin(math.radians(self.yaw + 90)) * acceleration
            self.velocity[2] += math.cos(math.radians(self.yaw + 90)) * acceleration
        if keys[K_d]:
            self.velocity[0] += math.sin(math.radians(self.yaw - 90)) * acceleration
            self.velocity[2] += math.cos(math.radians(self.yaw - 90)) * acceleration

        # Apply friction
        self.velocity[0] *= 0.9
        self.velocity[2] *= 0.9

        # Update position based on velocity
        self.position[0] += self.velocity[0]
        self.position[2] += self.velocity[2]

        # Handle jumping
        if keys[K_SPACE] and (self.position[1] == 0.0 or config.debug):  # Allow jumping only if on the ground
            self.vertical_velocity = self.jump_velocity

    def apply_gravity(self):
        self.vertical_velocity += self.gravity
        self.position[1] += self.vertical_velocity

        # Check for collision with the ground
        if self.position[1] < 0.25:  # Assuming the ground is at y = -1
            self.position[1] = 0.25
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
    
    def get_total_velocity(self):
        horizontal_velocity = math.sqrt(self.velocity[0]**2 + self.velocity[2]**2)
        total_velocity = math.sqrt(horizontal_velocity**2 + self.vertical_velocity**2)
        return total_velocity

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position[0], self.position[1] - self.height / 2, self.position[2])
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

