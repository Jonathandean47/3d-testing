import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Ground:
    @staticmethod
    def draw(player_position, render_distance=50, spacing=1):
        start_x = player_position[0] - (player_position[0] % spacing) - render_distance * spacing
        end_x = player_position[0] - (player_position[0] % spacing) + render_distance * spacing
        start_z = player_position[2] - (player_position[2] % spacing) - render_distance * spacing
        end_z = player_position[2] - (player_position[2] % spacing) + render_distance * spacing
        glBegin(GL_LINES)
        glColor3f(0.5, 0.5, 0.5)
        for x in range(int(start_x), int(end_x) + 1, spacing):
            glVertex3f(x, 0, start_z)
            glVertex3f(x, 0, end_z)
        for z in range(int(start_z), int(end_z) + 1, spacing):
            glVertex3f(start_x, 0, z)
            glVertex3f(end_x, 0, z)
        glEnd()