"""
Here is defined the structure of a bird in the simulation.
"""

import parameters as param
import math

class Bird:
    """The bird class"""

    birds_counter = 0

    def __init__(self, index: int, position: list, direction: list,
                 speed: float, acceleration: float):
        """
        Constructor for the bird class.

        :index: int, index that identifies bird.
        :position: list, coordinates (x,y,z) of bird
        :direction: list, direction of bird's velocity vector with coordinates (x,y,z)
        :speed: float, module of bird's velocity vector
        :acceleration: float, module of bird's acceleration vector
        :previous_vel: float, previous magnitude of velocity of bird
        """

        self.index = index
        self.position = position
        self.direction = direction
        self.speed = speed
        self.acceleration = acceleration
        self.previous_vel = previous_vel

        Bird.birds_counter += 1

    def __str__(self):
        """Returns display string"""
        return str(self.index) + " " + str(self.position) + " " + str(self.direction) + " " + str(self.speed) + " " + str(self.acceleration)

    def __repr__(self):
        """Returns representation string"""
        return str(self.index) + " " + str(self.position) + " " + str(self.direction) + " " + str(self.speed) + " " + str(self.acceleration)

    def __eq__(self, other_self):
        """Special comparison method.
        Returns True if birds are the same (based on index), False otherwise.
        """
        return self.index == other_self.index
    

    def countBirds(self):
        """Returns current number of birds in simulation"""
        return Bird.birds_counter

    def updatePos(self, diff_time):
        """Update bird's position using speed and direction.
        Takes into consideration boundary conditions"""

        new_x = self.position[0] + self.speed*self.direction[0]*diff_time
        new_y = self.position[1] + self.speed*self.direction[1]*diff_time
        ###new_z = self.position[2] + self.speed*self.direction[2]*diff_time
    
        # Apply boundary conditions
        if new_x < param.X_MIN - param.BOUNDARY_DELTA:
            new_x = param.X_MAX + param.BOUNDARY_DELTA
        elif new_x > param.X_MAX + param.BOUNDARY_DELTA:
            new_x = param.X_MIN - param.BOUNDARY_DELTA
        
        if new_y < param.Y_MIN - param.BOUNDARY_DELTA:
            new_y = param.Y_MAX + param.BOUNDARY_DELTA
        elif new_y > param.Y_MAX + param.BOUNDARY_DELTA:
            new_y = param.Y_MIN - param.BOUNDARY_DELTA

        ###if new_z < param.Z_MIN - param.BOUNDARY_DELTA:
        ###    new_z = param.Z_MAX + param.BOUNDARY_DELTA
        ###elif new_z > param.Z_MAX + param.BOUNDARY_DELTA:
        ###    new_z = param.Z_MIN - param.BOUNDARY_DELTA

        self.position[0] = new_x
        self.position[1] = new_y
        ###self.position[2] = new_z

    
    # def updateAcc(self, too_close_to_another_bird: bool):
    #     """Update bird's acceleration.
    #     Used when bird is too close to another bird."""

    #     self.acceleration = param.MIN_ACC + int(too_close_to_another_bird)*(param.MAX_ACC - param.MIN_ACC)


    def separation(self, neighbours: list):
        """Separate bird from neighbours that are too close."""
        if len(neighbours) == 0:
            return self.direction
        ###else:
            ### IMPLEMENT

    def cohesion(self, birds: list):
        """Update direction based on cohesion with other bird's positions.
        Bird will steer to move toward the average position of all birds."""
        if len(birds) == 0:
            return self.direction
        ###else:
            ### IMPLEMENT
    
    def alignment(self, birds: list):
        """Update direction based on cohesion with other bird's direction"""
        if len(birds) == 0:
            return self.direction
        ###else:
            ### IMPLEMENT
    
    def update(self, close_neighbours, all_birds):
        """Update direction, speed, acceleration and position, considering all rules."""

        self.previous_vel = [
            self.speed * self.direction[0],
            self.speed * self.direction[1]###,
            ###self.speed * self.direction[2]
        ]

        dir_separation = self.separation(close_neighbours)
        dir_cohesion = self.cohesion(all_birds)
        dir_alignment = self.alignment(all_birds)

        new_direction = [
            param.W_SEPARATION*dir_separation[0] + param.W_COHESION*dir_cohesion[0] + param.W_ALIGNMENT*dir_alignment[0],
            param.W_SEPARATION*dir_separation[1] + param.W_COHESION*dir_cohesion[1] + param.W_ALIGNMENT*dir_alignment[1]###,
            ###param.W_SEPARATION*dir_separation[2] + param.W_COHESION*dir_cohesion[2] + param.W_ALIGNMENT*dir_alignment[2],
        ]

        new_vel_x = self.speed*self.direction[0]+new_direction[0]*0.5   ### new_vel_x = self.speed*self.direction[0]+self.acceleration*new_direction[0]*0.1
        new_vel_y = self.speed*self.direction[1]+new_direction[1]*0.5
        ###new_vel_z = self.speed*self.direction[2]+new_direction[2]*0.5

        new_speed = math.sqrt(new_vel_x**2 + new_vel_y**2 + new_vel_z**2)

        self.direction = [
            new_vel_x/new_speed,
            new_vel_y/new_speed###,
            ###new_vel_z/new_speed
        ]

        if new_speed > param.MAX_VEL:
            new_speed = param.MAX_VEL
        elif new_speed < param.MIN_VEL:
            new_speed = param.MIN_VEL
        
        self.speed = new_speed

        self.updatePos(param.TIME_DELTA)




### Include acceleration
### Explain how direction of bird is defined, better
### To add obstacles and attractors: as birds, but add type parameter in __init__, to indicate if bird or obstacle or attractor
