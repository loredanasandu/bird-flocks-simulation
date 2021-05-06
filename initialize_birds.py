"""
Initialization of birds.
"""

import bird
import parameters as param
import math
import random

def generateBirds():
    """
    Generate a list of birds. Positions and velocity are random.
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

        birds.append(bird.Bird(i, position, direction, speed, obj_type=1))

    return birds


def generateAttractionPoints():
    """
    Generate a list of attraction points.
    """

    attraction_points = []
    i = param.NUM_BIRDS
    for point in param.ATTRACTION_POINTS:
        position = list(point)
        direction = [0]*param.DIM

        attraction_points.append(bird.Bird(i, position, direction, speed=0, obj_type=-1))

        i += 1

    return attraction_points


def generateRepulsionPoints():
    """
    Generate a list of repulsion points.
    """

    repulsion_points = []
    i = param.NUM_BIRDS + len(param.ATTRACTION_POINTS)
    for point in param.REPULSION_POINTS:
        position = list(point)
        direction = [0]*param.DIM

        repulsion_points.append(bird.Bird(i, position, direction, speed=0, obj_type=-2))

        i += 1

    return repulsion_points