"""
File that needs to be executed to run simulation.
"""

import parameters as param
import bird
import initialize_birds

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

import math
import time
import copy
import multiprocessing

manager = multiprocessing.Manager()

# Initialize window to display simulation
pygame.init()
window = pygame.display.set_mode((param.WIDTH, param.HEIGHT), DOUBLEBUF|OPENGL)
pygame.display.set_caption('Bird flock simulation')
glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
glClearColor(1,1,1,0)
pygame.display.flip()
clock = pygame.time.Clock()

# Initialize birds
###change
birds = manager.list()
birds.extend([copy.deepcopy(bird) for bird in initialize_birds.generateBirds()])

    
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
            glColor3fv((0.5,0.5,0.5))
            glVertex2fv(vertices[vertex])
            ###glVertex3fv(vertices[vertex])
    glEnd()


def draw_birds(birds):
    """ Draws the birds """

    ###rotate_x, rotate_y, rotate_z = 0,0,0
    
    copy_of_birds = (birds)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 0.0, 10.0)
                elif event.button == 5:
                    glTranslatef(0.0, 0.0, -10.0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    #reset birds
                    ### change
                    i = 0
                    for b in initialize_birds.generateBirds():
                        birds[i] = b
                        i += 1
                
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

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(1,1,1,0)

        draw_container()

        for bird in copy_of_birds:
            head = bird.position
            tail_centre = (bird.position[0]-22*bird.direction[0],
                           bird.position[1]-22*bird.direction[1]###,
                           ###bird.position[2]-22*bird.direction[2]
                          )

            temp_dir = []

            if bird.direction[1] != 0:
                temp_dir = [1, (-bird.direction[0])/(bird.direction[1])]
                ###temp_dir = [1, (-bird.direction[0])/(bird.direction[1]), 0]
            ###elif bird.direction[2] != 0:
            ###    temp_dir = [1, 1,(-bird.direction[0]-bird.direction[1])/bird.direction[2]]
            else:
                temp_dir = [(-bird.direction[1])/bird.direction[0],1]
                ###temp_dir = [(-bird.direction[1])/bird.direction[0],1,0]

            module = math.sqrt(temp_dir[0]**2+temp_dir[1]**2)
            temp_dir = [temp_dir[0]/module, temp_dir[1]/module]
            ###module = math.sqrt(temp_dir[0]**2+temp_dir[1]**2+temp_dir[2]**2)
            ###temp_dir = [temp_dir[0]/module, temp_dir[1]/module, temp_dir[2]/module]

            tail_square1 = (tail_centre[0]-8*temp_dir[0],
                           tail_centre[1]-8*temp_dir[1]###,
                           ###tail_centre[2]-8*temp_dir[2]
                           )
            tail_square2 = (tail_centre[0]+8*temp_dir[0],
                           tail_centre[1]+8*temp_dir[1]###,
                           ###tail_centre[2]+8*temp_dir[2]
                           )

            # Draw triangle
            glBegin(GL_TRIANGLES)
            glColor3fv((1,1,1))
            glVertex2fv((int(head[0]),int(head[1])))
            ###glVertex3fv((int(head[0]),int(head[1]),int(head[2])))
            glVertex2fv((int(tail_square1[0]),int(tail_square1[1])))
            ###glVertex3fv((int(tail_square1[0]),int(tail_square1[1]),int(tail_square1[2])))
            glVertex2fv((int(tail_square2[0]),int(tail_square2[1])))
            ###glVertex3fv((int(tail_square2[0]),int(tail_square2[1]),int(tail_square2[2])))
            glEnd()

        pygame.display.flip()

        clock.tick(30)  # 30 fps

def update_birds(birds,all_mates,close_neighbours):
    """Updates the birds' positions, directions, speed and acceleration"""

    while True:
        copy_close_neighbours = list(close_neighbours)
        copy_all_mates = list(all_mates)
        copy_birds = list(birds)

        i = 0
        for bird in copy_birds:
            bird.update(copy_close_neighbours[bird.index], copy_all_mates[bird.index])
            birds[i] = bird
            i += 1
        
def update_neighbours_and_mates(birds,all_mates,close_neighbours):
    """Updates the lists of close neighbours of each bird, and their flockmates."""
    
    all_mates_tmp = []
    close_neighbours_tmp = []

    while True:
        copy_birds = list(birds)
        for i in range(param.NUM_BIRDS):
            for bird in copy_birds:
                if bird.index == i or (bird.position[0] == copy_birds[i].position[0] and bird.position[1] == copy_birds[i].position[1]):    ###if bird.index == i or (bird.position[0] == copy_birds[i].position[0] and bird.position[1] == copy_birds[i].position[1] and bird.position[2] == copy_birds[i].position[2]):
                    continue
                all_mates_tmp.append(bird)
                if math.sqrt((copy_birds[i].position[0]-bird.position[0])**2+(copy_birds[i].position[1]-bird.position[1])**2)<param.MIN_DIST:   ###if math.sqrt((copy_birds[i].position[0]-bird.position[0])**2+(copy_birds[i].position[1]-bird.position[1])**2+(copy_birds[i].position[2]-bird.position[2])**2)<param.MIN_DIST
                    close_neighbours_tmp.append(bird)

                all_mates[i] = all_mates_tmp
                close_neighbours[i] = close_neighbours_tmp


if __name__ == '__main__':
    all_mates = manager.list()
    close_neighbours = manager.list()

    for i in range(param.NUM_BIRDS):
        all_mates.append([])
        close_neighbours.append([])

    pipe1 = multiprocessing.Process(target=update_birds, args=(birds,all_mates,close_neighbours))
    pipe2 = multiprocessing.Process(target=update_neighbours_and_mates, args=(birds,all_mates, close_neighbours))
    pipe3 = multiprocessing.Process(target=draw_birds, args=(birds))

    pipe2.start()
    pipe3.start()
    pipe1.start()

    pipe2.join()
    pipe3.join()
    pipe1.join()
