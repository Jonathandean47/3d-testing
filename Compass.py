import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

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
