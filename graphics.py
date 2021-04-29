"""
Functions used to render graphics.
"""

import parameters as param

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame
from pygame.locals import *

import numpy as np
import math


# Container's vertices and edges
if param.DIM == 2:  
    vertices = ((param.X_MAX, param.Y_MIN),
                (param.X_MAX, param.Y_MAX),
                (param.X_MIN, param.Y_MAX),
                (param.X_MIN, param.Y_MIN))

    edges = ((0,1), (1,2), (2,3), (3,0))

if param.DIM == 3:
    vertices = ((param.X_MAX, param.Y_MIN, param.Z_MIN),
                (param.X_MAX, param.Y_MAX, param.Z_MIN),
                (param.X_MIN, param.Y_MAX, param.Z_MIN),
                (param.X_MIN, param.Y_MIN, param.Z_MIN),
                (param.X_MAX, param.Y_MIN, param.Z_MAX),
                (param.X_MAX, param.Y_MAX, param.Z_MAX),
                (param.X_MIN, param.Y_MIN, param.Z_MAX),
                (param.X_MIN, param.Y_MAX, param.Z_MAX))

    edges = ((0,1),(0,3),(0,4),
            (2,1),(2,3),(2,7),
            (6,3),(6,4),(6,7),
            (5,1),(5,4),(5,7),)


def draw_container():
    """Draws 2D square or 3D cube that contains birds"""
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0,0,0))
            if param.DIM == 2:
                glVertex2fv(vertices[vertex])
            else:
                glVertex3fv(vertices[vertex])
    glEnd()


def initialize_window():
    pygame.init()
    display = (param.WIDTH, param.HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Bird flock simulation')

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glClearColor(1,1,1,0)
    pygame.display.flip()

    gluPerspective(45.0, (display[0]/display[1]), 1, 10000.0)
    glTranslatef(0,0,-2000.0)


def draw_triangle(head,tail_vertex1,tail_vertex2):
    glBegin(GL_TRIANGLES)
    glColor3fv((0,0,0))

    if param.DIM == 2:
        glVertex2fv((int(head[0]),int(head[1])))
        glVertex2fv((int(tail_vertex1[0]),int(tail_vertex1[1])))
        glVertex2fv((int(tail_vertex2[0]),int(tail_vertex2[1])))
    elif param.DIM == 3:
        glVertex3fv((int(head[0]),int(head[1]),int(head[2])))
        glVertex3fv((int(tail_vertex1[0]),int(tail_vertex1[1]),int(tail_vertex1[2])))
        glVertex3fv((int(tail_vertex2[0]),int(tail_vertex2[1]),int(tail_vertex2[2])))
    
    glEnd()


def draw_cone(pos, direction, radius, height, slices=7, stacks = 1):
    glColor3fv((0,0,0))

    z = np.array([0.0,0.0,1.0])

    # The axis of rotation is the cross product between z and the direction
    ax = np.cross(z,direction)

    # Module of direction (just in case)
    l_dir = math.sqrt(np.dot(direction,direction))
    angle = 180.0/math.pi * math.acos(np.dot(z,direction)/l_dir)

    glPushMatrix()
    glTranslatef(pos[0],pos[1],pos[2])
    glRotatef(angle,ax[0],ax[1],ax[2])
    glutSolidCone(radius, height, slices, stacks)
    #glutWireCone(radius, height, 5, stacks)
    glPopMatrix()


    