"""
File that needs to be executed to run simulation.
"""

import parameters as param
import bird
import initialize_birds
import graphics

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *

import math


assert param.DIM == 2 or param.DIM == 3
assert param.WIDTH == param.HEIGHT

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
graphics.initialize_window()
clock = pygame.time.Clock()

# Initialize birds
birds = initialize_birds.generateBirds()

# Initialize lists of neighbours and mates for each bird
all_mates = []
close_neighbours = []
for i in range(len(birds)):
    all_mates.append([])
    close_neighbours.append([])


# Run simulation
run = True
while run:
    rotate_x, rotate_y, rotate_z = 0,0,0


    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        # Zoom in and out with mouse's scroll wheel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                glTranslatef(0.0, 0.0, 10.0)
            elif event.button == 5:
                glTranslatef(0.0, 0.0, -10.0)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Leave
                pygame.quit()
                quit()
            if event.key == pygame.K_r:
                # Reset simulation
                birds = initialize_birds.generateBirds()

            if param.DIM == 3:
                # Rotations of cube if keys are pressed
                if event.key == pygame.K_w:
                    rotate_x = param.ROTATION
                if event.key == pygame.K_s:
                    rotate_x = -param.ROTATION
                if event.key == pygame.K_a:
                    rotate_y = param.ROTATION
                if event.key == pygame.K_d:
                    rotate_y = -param.ROTATION
                if event.key == pygame.K_q:
                    rotate_x = param.ROTATION
                if event.key == pygame.K_e:
                    rotate_x = -param.ROTATION
        
        if param.DIM == 3:
            # Stop rotations of cube if keys aren't pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    rotate_x = 0
                if event.key == pygame.K_s:
                    rotate_x = 0
                if event.key == pygame.K_a:
                    rotate_y = 0
                if event.key == pygame.K_d:
                    rotate_y = 0
                if event.key == pygame.K_q:
                    rotate_x = 0
                if event.key == pygame.K_e:
                    rotate_x = 0


    if param.DIM == 3:
        # Rotate cube
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        glRotatef(rotate_z, 0, 0, 1)


    # Draw container
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClearColor(1,1,1,0)

    graphics.draw_container()



    # Update lists of neighbours and mates

    for i in range(len(birds)):
        for bird in birds:
            if param.DIM == 2:
                if bird.index == birds[i].index or (bird.position[0] == birds[i].position[0] and bird.position[1] == birds[i].position[1]):
                    continue
                all_mates[i].append(bird)
                if math.sqrt((birds[i].position[0]-bird.position[0])**2+(birds[i].position[1]-bird.position[1])**2)<param.MIN_DIST:
                    close_neighbours[i].append(bird)
            elif param.DIM == 3:
                if bird.index == birds[i].index or (bird.position[0] == birds[i].position[0] and bird.position[1] == birds[i].position[1] and bird.position[2] == birds[i].position[2]):
                    continue
                all_mates[i].append(bird)
                if math.sqrt((birds[i].position[0]-bird.position[0])**2+(birds[i].position[1]-bird.position[1])**2+(birds[i].position[2]-bird.position[2])**2)<param.MIN_DIST:
                    close_neighbours[i].append(bird)



    # Draw birds
    if param.DIM == 2:
        for bird in birds:
            head = bird.position
            tail_centre = (bird.position[0]-18*bird.direction[0],
                        bird.position[1]-18*bird.direction[1]
                        )


            perp_vector = [bird.direction[1],
                        -bird.direction[0]
                        ]

            tail_vertex1 = (tail_centre[0]-6*perp_vector[0],
                            tail_centre[1]-6*perp_vector[1]
                            )
            tail_vertex2 = (tail_centre[0]+6*perp_vector[0],
                            tail_centre[1]+6*perp_vector[1]
                            )


            # Draw triangle
            graphics.draw_triangle(head,tail_vertex1,tail_vertex2)

    elif param.DIM == 3:
        for bird in birds:
            head = bird.position
            
            # Draw cone
            graphics.draw_cone(pos = head, direction = bird.direction, radius = 6, height = 18)



    # Update birds

    for i in range(len(birds)):
        birds[i].update(close_neighbours[i],birds)

    pygame.display.flip()
    clock.tick(param.FPS)


pygame.quit()
quit()