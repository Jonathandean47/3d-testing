import numpy
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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

