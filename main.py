import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

def draw_cube():
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
    edges = (
        (0,1),
        (0,3),
        (0,4),
        (2,1),
        (2,3),
        (2,7),
        (6,3),
        (6,4),
        (6,7),
        (5,1),
        (5,4),
        (5,7)
    )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_plane():
    glColor3f(0.0, 1.0, 0.0)  # Set the color to green
    glBegin(GL_QUADS)
    glVertex3f(-10, -1, -10)
    glVertex3f(10, -1, -10)
    glVertex3f(10, -1, 10)
    glVertex3f(-10, -1, 10)
    glEnd()

def main():
    init()
    clock = pygame.time.Clock()
    move_speed = 0.1
    mouse_sensitivity = 0.1
    yaw, pitch = -90.0, 0.0  # Initialize yaw to -90.0 to face the cube initially
    camera_pos = [0, 0, 0]
    camera_front = [0, 0, -1]
    camera_up = [0, 1, 0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_pos[0] += camera_front[0] * move_speed
            camera_pos[1] += camera_front[1] * move_speed
            camera_pos[2] += camera_front[2] * move_speed
        if keys[pygame.K_s]:
            camera_pos[0] -= camera_front[0] * move_speed
            camera_pos[1] -= camera_front[1] * move_speed
            camera_pos[2] -= camera_front[2] * move_speed
        if keys[pygame.K_a]:
            camera_pos[0] -= math.cos(math.radians(yaw - 90)) * move_speed
            camera_pos[2] -= math.sin(math.radians(yaw - 90)) * move_speed
        if keys[pygame.K_d]:
            camera_pos[0] += math.cos(math.radians(yaw - 90)) * move_speed
            camera_pos[2] += math.sin(math.radians(yaw - 90)) * move_speed
        if keys[pygame.K_SPACE]:
            camera_pos[1] += move_speed
        if keys[pygame.K_c]:
            camera_pos[1] -= move_speed

        mouse_movement = pygame.mouse.get_rel()
        yaw += mouse_movement[0] * mouse_sensitivity
        pitch -= mouse_movement[1] * mouse_sensitivity

        # Constrain the pitch
        if pitch > 89.0:
            pitch = 89.0
        if pitch < -89.0:
            pitch = -89.0

        # Calculate the new front vector
        front = [
            math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)),
            math.sin(math.radians(pitch)),
            math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
        ]
        camera_front = [front[0], front[1], front[2]]

        glLoadIdentity()
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
                  camera_pos[0] + camera_front[0], camera_pos[1] + camera_front[1], camera_pos[2] + camera_front[2],
                  camera_up[0], camera_up[1], camera_up[2])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # draw_plane()
        draw_cube()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
