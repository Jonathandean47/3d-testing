import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from Cube import *
from Player import *
from Compass import *
from Ground import *

# Initialize Pygame and OpenGL
def init_pygame_opengl(render_distance=50.0):
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(72, (display[0] / display[1]), 0.001, render_distance)  # Adjusted FOV angle and aspect ratio
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