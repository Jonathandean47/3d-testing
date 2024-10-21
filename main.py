import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from Cube import *
from Player import *
from Compass import *
from Ground import *
from util import *
import sys

def main():
    render_distance = 50
    frame_rate = 60
    clock = pygame.time.Clock()
    display = init_pygame_opengl(render_distance)
    config = load_config()
    
    check_opengl_errors()

    # Create player
    player = Player(position=(0, 0.5, 5), speed=0.02, gravity=-0.01, jump_velocity=0.1)

    # Create objects
    objects = [
        Cube((0, 1, 0), size=1),
        Cube((3, 2, 0), size=2),
        Cube((-2, 0.5, 0), size=0.5)
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

        # Check for collisions and adjust player position
        player_bounding_box = player.get_bounding_box()
        for obj in objects:
            obj_bounding_box = obj.get_bounding_box()
            if check_object_collision(player_bounding_box, obj_bounding_box):
                collision_point = calculate_collision_point(player.position, player.velocity, obj_bounding_box)
                if collision_point:
                    # Calculate the surface normal at the collision point
                    normal = calculate_surface_normal_at_point(collision_point, obj)
                    if normal is not None:
                        # Calculate the angle between the surface normal and the vertical axis
                        angle = calculate_angle(normal)

                        # Reduce the player's velocity based on the angle
                        reduction_factor = max(0, 1 - (angle / 90))  # Scale from 1 (0 degrees) to 0 (90 degrees)
                        player.velocity[0] *= reduction_factor
                        player.velocity[2] *= reduction_factor

                        # Calculate the reflection vector
                        movement_vector = numpy.array([player.velocity[0], 0, player.velocity[2]])
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

        # Apply friction to reduce speed
        player.velocity[0] *= 0.9
        player.velocity[2] *= 0.9

        # Clear screen and reset view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(*player.get_view_matrix())

        # Draw ground based on player's position
        Ground.draw(player.position, render_distance)

        # Draw objects
        for obj in objects:
            obj.draw()

        # Draw player
        player.draw()

        if config["debug"]["show_compass"]:
            # Draw compass
            Compass.draw(player.yaw, player.pitch)
            # Switch to orthographic projection to draw text
        if config["debug"]["extended_info"]:
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluOrtho2D(0, display[0], 0, display[1])
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            # Draw camera position
            draw_text((10, 10), f"({player.position[0]:.2f}, {player.position[1]:.2f}, {player.position[2]:.2f})")
            draw_text((display[0] - 180, 10), f"({player.yaw:.2f}°, {-player.pitch:.2f}°)")
            # Draw total velocity
            total_velocity = player.get_total_velocity()
            draw_text((10, 30), f"Velocity: {total_velocity:.2f}")
            # Restore perspective projection
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix()

        pygame.display.flip()
        clock.tick(frame_rate)

    pygame.quit()

if __name__ == "__main__":
    main()
    sys.exit()