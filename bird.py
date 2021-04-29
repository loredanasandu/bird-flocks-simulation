"""
Here is defined the structure of a bird in the simulation.
"""

import parameters as param
import math
import statistics

class Bird:
    """The bird class"""

    birds_counter = 0

    def __init__(self, index: int, position: list, direction: list,
                 speed: float, acceleration: float):
        """
        Constructor for the bird class.

        :index: int, index that identifies bird.
        :position: list, coordinates (x,y,z) of bird
        :direction: list, direction of bird's velocity vector with coordinates (x,y,z), as a unit vector
        :speed: float, module of bird's velocity vector
        :previous_vel: float, previous magnitude of velocity of bird
        """

        self.index = index
        self.position = position
        self.direction = direction
        self.speed = speed
        self.previous_vel = 0

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

        ###IMPLEMENT
        # Apply boundary conditions
        if new_x < param.X_MIN + param.BOUNDARY_DELTA:
            new_x = param.X_MAX + param.BOUNDARY_DELTA
        elif new_x > param.X_MAX - param.BOUNDARY_DELTA:
            new_x = param.X_MIN - param.BOUNDARY_DELTA
        
        if new_y < param.Y_MIN + param.BOUNDARY_DELTA:
            new_y = param.Y_MAX + param.BOUNDARY_DELTA
        elif new_y > param.Y_MAX - param.BOUNDARY_DELTA:
            new_y = param.Y_MIN - param.BOUNDARY_DELTA

        ###if new_z < param.Z_MIN - param.BOUNDARY_DELTA:
        ###    new_z = param.Z_MAX + param.BOUNDARY_DELTA
        ###elif new_z > param.Z_MAX + param.BOUNDARY_DELTA:
        ###    new_z = param.Z_MIN - param.BOUNDARY_DELTA

        self.position[0] = new_x
        self.position[1] = new_y
        ###self.position[2] = new_z

    
    def separation(self, neighbours: list):     # Avoidance
        """Separate bird from neighbours that are too close."""
        if len(neighbours) == 0:
            return self.direction
        else:
            avoidance_dir = [
                0,0###,
                ###0
            ]

            for i in range(len(neighbours)):
                dist = [
                    neighbours[i].position[0]-self.position[0],
                    neighbours[i].position[1]-self.position[1]###,
                    ###neighbours[i].position[2]-self.position[2]
                ]
                
                mod_dist = math.sqrt(dist[0]**2+dist[1]**2)
                ###mod_dist = math.sqrt(dist[0]**2+dist[1]**2+dist[2]**2)

                avoidance_dir[0] += (param.MIN_DIST - mod_dist)*dist[0]
                avoidance_dir[1] += (param.MIN_DIST - mod_dist)*dist[1]
                ###avoidance_dir[2] += (param.MIN_DIST - mod_dist)*dist[2]

            avoidance_dir[0] *= (-1/len(neighbours))
            avoidance_dir[1] *= (-1/len(neighbours))
            ###avoidance_dir[2] *= (-1/len(neighbours))

            return avoidance_dir


    def cohesion(self, birds: list):     # Centre
        """Update direction based on cohesion with other bird's positions.
        Bird will change direction to move toward the average position of all birds."""
        if len(birds) == 0:
            return self.direction
        else:
            avg_x = statistics.mean([bird.position[0] for bird in birds])
            avg_y = statistics.mean([bird.position[1] for bird in birds])
            ###avg_z = statistics.mean([bird.position[2] for bird in birds])

            centre = [
                avg_x, avg_y###, avg_z
            ]

            dir_centre = [
                centre[0] - self.position[0], 
                centre[1] - self.position[1]###,
                ###centre[2] - self.position[2]
            ]

            return dir_centre

    

    def alignment(self, birds: list):   # Copy
        """Update direction based on cohesion with other bird's directions."""
        if len(birds) == 0:
            return self.direction
        else:
            avg_direction =[
                0,0###,
                ###0
            ]

            for i in range(len(birds)):
                avg_direction[0] += birds[i].direction[0]
                avg_direction[1] += birds[i].direction[1]
                ###avg_direction[2] += birds[i].direction[2]
    
            avg_direction[0] = avg_direction[0]/len(birds)
            avg_direction[1] = avg_direction[1]/len(birds)
            ###avg_direction[2] = avg_direction[2]/len(birds)

            return avg_direction


    def update(self, close_neighbours, all_birds):
        """Updates direction, speed and position, considering all rules."""

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

        new_vel_x = self.speed*self.direction[0] + new_direction[0]*MU   ### new_vel_x = self.speed*self.direction[0]+self.acceleration*new_direction[0]*0.1
        new_vel_y = self.speed*self.direction[1] + new_direction[1]*MU
        ###new_vel_z = self.speed*self.direction[2]+new_direction[2]*0.5

        new_speed = math.sqrt(new_vel_x**2 + new_vel_y**2)
        ###new_speed = math.sqrt(new_vel_x**2 + new_vel_y**2 + new_vel_z**2)

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
