import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from Cube import *
from Player import *
from Compass import *
from Ground import *
import json

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Initialize Pygame and OpenGL
def init_pygame_opengl(render_distance=50.0):
    pygame.init()
    # Load and set the window icon
    # icon_image = pygame.image.load(".\\assets\\icon.jpeg")
    # pygame.display.set_icon(icon_image)
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    display = (screen_width, screen_height)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(60, (display[0] / display[1]), 0.001, render_distance)  # Adjusted FOV angle and aspect ratio
    glEnable(GL_DEPTH_TEST)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    return display

def draw_text(position, text_string):
    font = pygame.font.SysFont("Arial", 18)
    text_surface = font.render(text_string, True, (255, 255, 255, 255), (0, 0, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
def check_object_collision(bounding_box1, bounding_box2):
    min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = bounding_box1
    min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = bounding_box2

    if (max_x1 >= min_x2 and min_x1 <= max_x2 and
        max_y1 >= min_y2 and min_y1 <= max_y2 and
        max_z1 >= min_z2 and min_z1 <= max_z2):
        return True
    return False

def reflect_vector(vector, normal):
    return vector - 2 * numpy.dot(vector, normal) * normal

def check_opengl_errors():
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL Error: {gluErrorString(error)}")
        
def calculate_angle(normal):
    vertical = numpy.array([0, 1, 0])
    dot_product = numpy.dot(normal, vertical)
    angle = math.degrees(math.acos(dot_product))
    return angle

def calculate_collision_point(player_position, player_velocity, obj_bounding_box):
    # Simple bounding box collision detection for demonstration
    # You can replace this with more precise collision detection logic
    collision_point = None
    if (player_position[0] + player_velocity[0] >= obj_bounding_box[0] and
        player_position[0] + player_velocity[0] <= obj_bounding_box[1] and
        player_position[2] + player_velocity[2] >= obj_bounding_box[4] and
        player_position[2] + player_velocity[2] <= obj_bounding_box[5]):
        collision_point = [player_position[0] + player_velocity[0], player_position[1], player_position[2] + player_velocity[2]]
    return collision_point

def calculate_surface_normal_at_point(collision_point, obj):
    for i, surface in enumerate(obj.surfaces):
        if point_in_surface(collision_point, surface, obj.vertices):
            return obj.get_surface_normal(i)
    return None

def point_in_surface(point, surface, vertices):
    # Simple check to see if the point is within the surface
    # You can replace this with more precise point-in-polygon checks
    v1 = vertices[surface[0]]
    v2 = vertices[surface[1]]
    v3 = vertices[surface[2]]
    v4 = vertices[surface[3]]
    return (min(v1[0], v2[0], v3[0], v4[0]) <= point[0] <= max(v1[0], v2[0], v3[0], v4[0]) and
            min(v1[2], v2[2], v3[2], v4[2]) <= point[2] <= max(v1[2], v2[2], v3[2], v4[2]))