"""
.. module:: initialize_birds

Initialization of birds.
"""

import bird
import parameters as param
import math
import random


def generateBirds():
    """
    Generates a list of birds. Positions and velocity are random.

    :return: list of instances of the class :class:`bird.Bird`.
    :rtype: list

    |
    """

    birds = []
    for i in range(param.NUM_BIRDS):
        if param.DIM == 2:
            position = [
                random.randint(param.X_MIN+param.BOUNDARY_DELTA, param.X_MAX-param.BOUNDARY_DELTA),
                random.randint(param.Y_MIN+param.BOUNDARY_DELTA, param.Y_MAX-param.BOUNDARY_DELTA)
            ]
        elif param.DIM == 3:
            position = [
                random.randint(param.X_MIN+param.BOUNDARY_DELTA, param.X_MAX-param.BOUNDARY_DELTA),
                random.randint(param.Y_MIN+param.BOUNDARY_DELTA, param.Y_MAX-param.BOUNDARY_DELTA),
                random.randint(param.Z_MIN, param.Z_MAX)
            ]


        # to place along a line: position[1], position[2] = 0,0
        position[1] = 0
        if param.DIM == 3:
            position[2] = 0
        
        
        speed = random.randint(param.MIN_VEL, param.MAX_VEL)

        if param.DIM == 2:
            direction_x = random.choice([-1,1])*random.random()
            direction_y = random.choice([-1,1])*math.sqrt(1-direction_x**2)

            direction = [direction_x, direction_y]

        else:
            direction_x = random.choice([-1,1])*random.random()

            direction_y = random.random()
            while direction_x**2 + direction_y**2 >= 1:
                direction_y = random.random()
            direction_y = random.choice([-1,1])*direction_y

            direction_z = random.choice([-1,1])*math.sqrt(1-direction_x**2-direction_y**2)
            
            direction = [direction_x, direction_y, direction_z]

        birds.append(bird.Bird(i, position, direction, speed, type=1))

    return birds


def generateAttractionPoints():
    """
    Generates a list of attraction points.

    :return: list of instances of the class :class:`bird.Bird`, with the attribute :py:data:`type` assigned to -1 (which represents an Attraction Point).
    :rtype: list

    |
    """

    attraction_points = []
    i = param.NUM_BIRDS
    for point in param.ATTRACTION_POINTS:

        position = list(point)
        speed = random.randint(param.MIN_VEL, param.MAX_VEL)

        if param.DIM == 2:
            direction_x = random.choice([-1,1])*random.random()
            direction_y = random.choice([-1,1])*math.sqrt(1-direction_x**2)

            direction = [direction_x, direction_y]

        else:
            direction_x = random.choice([-1,1])*random.random()

            direction_y = random.random()
            while direction_x**2 + direction_y**2 >= 1:
                direction_y = random.random()
            direction_y = random.choice([-1,1])*direction_y

            direction_z = random.choice([-1,1])*math.sqrt(1-direction_x**2-direction_y**2)
            
            direction = [direction_x, direction_y, direction_z]

        attraction_points.append(bird.Bird(i, position, direction, speed, type=-1))

        i += 1

    return attraction_points


def generateRepulsionPoints():
    """
    Generates a list of repulsion points.

    :return: list of instances of the class :class:`bird.Bird`, with the attribute :py:data:`type` assigned to -2 (which represents an Repulsion Point).
    :rtype: list

    |
    """

    repulsion_points = []
    i = param.NUM_BIRDS + len(param.ATTRACTION_POINTS)
    for point in param.REPULSION_POINTS:

        position = list(point)
        speed = random.randint(param.MIN_VEL, param.MAX_VEL)

        if param.DIM == 2:
            direction_x = random.choice([-1,1])*random.random()
            direction_y = random.choice([-1,1])*math.sqrt(1-direction_x**2)

            direction = [direction_x, direction_y]

        else:
            direction_x = random.choice([-1,1])*random.random()

            direction_y = random.random()
            while direction_x**2 + direction_y**2 >= 1:
                direction_y = random.random()
            direction_y = random.choice([-1,1])*direction_y

            direction_z = random.choice([-1,1])*math.sqrt(1-direction_x**2-direction_y**2)
            
            direction = [direction_x, direction_y, direction_z]

        repulsion_points.append(bird.Bird(i, position, direction, speed, type=-2))

        i += 1

    return repulsion_points
