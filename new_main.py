"""
File that needs to be executed to run simulation.
"""

import parameters as param
import bird
import initialize_birds

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

import sys
import math


##### ASSERT DIM == 2,3; WIDTH == HEIGHT

# DRAW CONTAINER
#2D          
vertices = ((param.X_MAX, param.Y_MIN),
            (param.X_MAX, param.Y_MAX),
            (param.X_MIN, param.Y_MAX),
            (param.X_MIN, param.Y_MIN))

edges = ((0,1), (1,2), (2,3), (3,0))

###3D
# vertices = ((param.X_MAX, param.Y_MIN, param.Z_MIN),
#             (param.X_MAX, param.Y_MAX, param.Z_MIN),
#             (param.X_MIN, param.Y_MAX, param.Z_MIN),
#             (param.X_MIN, param.Y_MIN, param.Z_MIN),
#             (param.X_MAX, param.Y_MIN, param.Z_MAX),
#             (param.X_MAX, param.Y_MAX, param.Z_MAX),
#             (param.X_MIN, param.Y_MIN, param.Z_MAX),
#             (param.X_MIN, param.Y_MAX, param.Z_MAX))

# edges = ((0,1),(0,3),(0,4),
#          (2,1),(2,3),(2,7),
#          (6,3),(6,4),(6,7),
#          (5,1),(5,4),(5,7),)

def draw_container():
    """Draws 2D square or 3D cube that contains birds"""
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0,0,0))
            glVertex2fv(vertices[vertex])
            ###glVertex3fv(vertices[vertex])
    glEnd()



# Initialize window to display simulation
pygame.init()
display = (param.WIDTH, param.HEIGHT)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
pygame.display.set_caption('Bird flock simulation')

glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glClearColor(1,1,1,0)
pygame.display.flip()

gluPerspective(45.0, (display[0]/display[1]), 1, 10000.0)
glTranslatef(0,0,-2000.0)

clock = pygame.time.Clock()



# Initialize birds
birds = initialize_birds.generateBirds()


# Initialize lists of neighbours and mates for each bird
all_mates = []                  ### NEEDED?
close_neighbours = []
for i in range(len(birds)):
    all_mates.append([])
    close_neighbours.append([])


# Run simulation
run = True
while run:
    ###rotate_x, rotate_y, rotate_z = 0,0,0


    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
         # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 4:
        #         glTranslatef(0.0, 0.0, 10.0)
        #     elif event.button == 5:
        #         glTranslatef(0.0, 0.0, -10.0)
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_ESCAPE:
        #         pygame.quit()
        #         sys.exit()
        #     if event.key == pygame.K_r:
        #         #reset birds
        #         ### change
        #         i = 0
        #         for b in initialize_birds.generateBirds():
        #             birds[i] = b
        #             i += 1
            
            ### ROTATIONS
            # if event.key == pygame.K_w:
            #     rotate_x = 5
            # if event.key == pygame.K_s:
            #     rotate_x = -5
            # if event.key == pygame.K_a:
            #     rotate_y = 5
            # if event.key == pygame.K_d:
            #     rotate_y = -5
            # if event.key == pygame.K_q:
            #     rotate_x = 5
            # if event.key == pygame.K_e:
            #     rotate_x = -5
        
        ### ROTATIONS
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_w:
        #         rotate_x = 0
        #     if event.key == pygame.K_s:
        #         rotate_x = 0
        #     if event.key == pygame.K_a:
        #         rotate_y = 0
        #     if event.key == pygame.K_d:
        #         rotate_y = 0
        #     if event.key == pygame.K_q:
        #         rotate_x = 0
        #     if event.key == pygame.K_e:
        #         rotate_x = 0

    ### ROTATIONS
    # glRotatef(rotate_x, 1, 0, 0)
    # glRotatef(rotate_y, 0, 1, 0)
    # glRotatef(rotate_z, 0, 0, 1)

    # Draw container
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClearColor(1,1,1,0)

    draw_container()

    # Update lists of neighbours and mates

    for i in range(len(birds)):
        for bird in birds:
            if bird.index == birds[i].index:# or (bird.position[0] == birds[i].position[0] and bird.position[1] == birds[i].position[1]):
            ### if bird.index == birds[i].index or (bird.position[0] == birds[i].position[0] and bird.position[1] == birds[i].position[1] and bird.position[2] == birds[i].position[2]):
                continue
            #all_mates[i].append(bird)
            if math.sqrt((birds[i].position[0]-bird.position[0])**2+(birds[i].position[1]-bird.position[1])**2)<param.MIN_DIST:
            ### if math.sqrt((birds[i].position[0]-bird.position[0])**2+(birds[i].position[1]-bird.position[1])**2+(birds[i].position[2]-bird.position[2])**2)<param.MIN_DIST:
                close_neighbours[i].append(bird)
    
    # Draw birds

    for bird in birds:
        head = bird.position
        tail_centre = (bird.position[0]-18*bird.direction[0],
                       bird.position[1]-18*bird.direction[1]###,
                       ###bird.position[2]-22*bird.direction[2]
                      )


        perp_vector = [bird.direction[1],
                       -bird.direction[0]
                      ]
        #### 3d mirárselo

        tail_vertex1 = (tail_centre[0]-6*perp_vector[0],
                        tail_centre[1]-6*perp_vector[1]###,
                        ###tail_centre[2]-8*temp_dir[2]
                        )
        tail_vertex2 = (tail_centre[0]+6*perp_vector[0],
                        tail_centre[1]+6*perp_vector[1]###,
                        ###tail_centre[2]+8*temp_dir[2]
                        )


        # Draw triangle
        glBegin(GL_TRIANGLES)
        glColor3fv((0,0,0))
        glVertex2fv((int(head[0]),int(head[1])))
        ###glVertex3fv((int(head[0]),int(head[1]),int(head[2])))
        glVertex2fv((int(tail_vertex1[0]),int(tail_vertex1[1])))
        ###glVertex3fv((int(tail_vertex1[0]),int(tail_vertex1[1]),int(tail_vertex1[2])))
        glVertex2fv((int(tail_vertex2[0]),int(tail_vertex2[1])))
        ###glVertex3fv((int(tail_vertex2[0]),int(tail_vertex2[1]),int(tail_vertex2[2])))
        glEnd()



    # Update birds

    for i in range(len(birds)):
        birds[i].update(close_neighbours[i],birds)

    pygame.display.flip()
    clock.tick(param.FPS)



pygame.quit()
quit()