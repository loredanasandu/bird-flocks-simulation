"""
.. module:: graphics

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

    edges = ((0, 1), (1, 2), (2, 3), (3, 0))

if param.DIM == 3:
    vertices = ((param.X_MAX, param.Y_MIN, param.Z_MIN),
                (param.X_MAX, param.Y_MAX, param.Z_MIN),
                (param.X_MIN, param.Y_MAX, param.Z_MIN),
                (param.X_MIN, param.Y_MIN, param.Z_MIN),
                (param.X_MAX, param.Y_MIN, param.Z_MAX),
                (param.X_MAX, param.Y_MAX, param.Z_MAX),
                (param.X_MIN, param.Y_MIN, param.Z_MAX),
                (param.X_MIN, param.Y_MAX, param.Z_MAX))

    edges = ((0, 1), (0, 3), (0, 4),
             (2, 1), (2, 3), (2, 7),
             (6, 3), (6, 4), (6, 7),
             (5, 1), (5, 4), (5, 7),)


def draw_container():
    """
    Draws 2D square or 3D cube that contains birds.

    |
    """
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glColor3fv((0, 0, 0))
            if param.DIM == 2:
                glVertex2fv(vertices[vertex])
            else:
                glVertex3fv(vertices[vertex])
    glEnd()


def initialize_window():
    """
    Initializes window where simulation will be shown when running the program.

    |
    """

    pygame.init()
    display = (param.WIDTH, param.HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Bird flock simulation')

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1, 1, 1, 0)
    pygame.display.flip()

    gluPerspective(45.0, (display[0]/display[1]), 1, 10000.0)
    glTranslatef(0, 0, -2000.0)


def draw_triangle(head, tail_vertex1, tail_vertex2):
    """
    Draws a black triangle inisde the container.

    :param head: coordinates of the triangle's head vertex.
    :type head: list
    :param tail_vertex1: coordinates of a tail's vertex.
    :type tail_vertex1: list
    :param tail_vertex2: coordinates of the other tail's vertex.
    :type tail_vertex2: list

    |
    """

    glBegin(GL_TRIANGLES)
    glColor3fv((0, 0, 0))

    if param.DIM == 2:
        glVertex2fv((int(head[0]), int(head[1])))
        glVertex2fv((int(tail_vertex1[0]), int(tail_vertex1[1])))
        glVertex2fv((int(tail_vertex2[0]), int(tail_vertex2[1])))
    elif param.DIM == 3:
        glVertex3fv((int(head[0]), int(head[1]), int(head[2])))
        glVertex3fv((int(tail_vertex1[0]), int(
            tail_vertex1[1]), int(tail_vertex1[2])))
        glVertex3fv((int(tail_vertex2[0]), int(
            tail_vertex2[1]), int(tail_vertex2[2])))

    glEnd()


def draw_cone(pos, direction, radius, height, slices=7, stacks=1):
    """
    Draws a black cone inisde the container.

    :param pos: coordinates of the cone's head vertex.
    :type pos: list
    :param direction: unitary vector that represents the direction in wich the cone is pointed.
    :type direction: list
    :param radius: radius of the cones base, in pixels.
    :type radius: int
    :param height: height of the cone, in pixels.
    :type height: int
    :param slices: Number of slices that will determine the cone's shape in the graphics, defaults to 7.
    :type slices: int, optional
    :param stacks: Number of stacks that will determine the cone's shape in the graphics, defaults to 1.
    :type stacks: int, optional

    |
    """
    
    glColor3fv((0, 0, 0))

    z = np.array([0.0, 0.0, 1.0])

    # The axis of rotation is the cross product between z and the direction
    ax = np.cross(z, direction)

    # Module of direction (just in case)
    l_dir = math.sqrt(np.dot(direction, direction))
    angle = 180.0/math.pi * math.acos(np.dot(z, direction)/l_dir)

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(angle, ax[0], ax[1], ax[2])
    glutSolidCone(radius, height, slices, stacks)
    #glutWireCone(radius, height, 5, stacks)
    glPopMatrix()


def draw_circle(position, color, radius=10, side_num=10):
    """
    Draws a circle of a given color.

    :param position: coordinates of the circle's center point.
    :type position: list
    :param color: the color of the circle. For example: 'red', 'green'.
    :type color: str
    :param radius: radius of the circle (in pixels), defaults to 10.
    :type radius: int, optional
    :param side_num: radius of the circle (in pixels), defaults to 10.
    :type side_num: int, optional

    |
    """
    
    
    if color == 'red':
        glColor3fv((1.0, 0, 0))
    elif color == 'green':
        glColor3fv((0, 0.54, 0.06))
    else:
        glColor3fv((0, 0, 0))

    glBegin(GL_POLYGON)

    for vertex in range(0, side_num):
        angle = float(vertex) * 2.0 * np.pi / side_num
        glVertex2f(position[0]+np.cos(angle)*radius, position[1]+np.sin(angle)*radius)

    glEnd()


def draw_sphere(position,color,r=10,lats=10,longs=10):
    """
    Draws a sphere of a given color.

    :param position: coordinates of the sphere's center point.
    :type position: list
    :param color: the color of the sphere. For example: 'red', 'green'
    :type color: str
    :param r: radius of the sphere (in pixels), defaults to 10.
    :type r: int, optional
    :param lats: number of lats that will determine the sphere's shape in the graphics, defaults to 10.
    :type lats: int, optional
    :param longs: number of longs that will determine the sphere's shape in the graphics, defaults to 10.
    :type longs: int, optional

    |
    """

    if color == 'red':
        glColor3fv((1.0, 0, 0))
    elif color == 'green':
        glColor3fv((0, 0.54, 0.06))
    else:
        glColor3fv((0, 0, 0))

    for i in range(lats+1):
        lat1 = math.pi*(-1/2 + (i-1)/lats)
        z1 =math.sin(lat1)
        zr1 = math.cos(lat1)

        lat2 = math.pi*(-1/2 + i/lats)
        z2 = math.sin(lat2)
        zr2 = math.cos(lat2)

        glBegin(GL_QUAD_STRIP)
        for j in range(longs+1):
            _long = 2*math.pi*(j-1)/longs
            x = math.cos(_long)
            y = math.sin(_long)

            glNormal3f(position[0] + x*zr1, position[1] + y*zr1, position[2] + z1)
            glVertex3f(position[0] + r*x*zr1, position[1] + r*y*zr1, position[2] + r*z1)
            glNormal3f(position[0] + x*zr2, position[1] + y*zr2, position[2] + z2)
            glVertex3f(position[0] + r*x*zr2, position[1] + r*y*zr2, position[2] + r*z2)
        
        glEnd()