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
        position = [
            random.randint(param.X_MIN, param.X_MAX),
            random.randint(param.Y_MIN,param.Y_MAX)###,
            ###random.randint(param.Z_MIN, param.Z_MAX)
        ]


        ### para poner en una línea: position[1], position[2] = 0,0

        speed = random.randint(param.MIN_VEL, param.MAX_VEL)


        direction_x = random.choice([-1,1])*random.random()

        direction_y = random.random()
        while direction_x**2 + direction_y**2 >= 1:
            direction_y = random.random()
        direction_y = random.choice([-1,1])*direction_y

        direction_z = random.choice([-1,1])*math.sqrt(1-direction_x**2-direction_y**2)
        
        direction = [direction_x, direction_y, direction_z]


        birds.append(bird.Bird(i, position, direction, speed, 0))


    return birds


#### generate obstacles and attractors