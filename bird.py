"""
Here is defined the structure of a bird in the simulation.
"""

import parameters as param
import math
import statistics

class Bird:
    """The bird class"""

    def __init__(self, index: int, position: list, direction: list, speed: float):
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


    def updatePos(self, diff_time):
        """Update bird's position using speed and direction.
        Takes into consideration boundary conditions"""

        new_pos = [self.position[i] + self.speed*self.direction[i]*diff_time for i in range(param.DIM)]

        # Apply boundary conditions
        if new_pos[0] < param.X_MIN + param.BOUNDARY_DELTA:
            new_pos[0] = param.X_MAX - param.BOUNDARY_DELTA
        elif new_pos[0] > param.X_MAX - param.BOUNDARY_DELTA:
            new_pos[0] = param.X_MIN + param.BOUNDARY_DELTA
        
        if new_pos[1] < param.Y_MIN + param.BOUNDARY_DELTA:
            new_pos[1] = param.Y_MAX - param.BOUNDARY_DELTA
        elif new_pos[1] > param.Y_MAX - param.BOUNDARY_DELTA:
            new_pos[1] = param.Y_MIN + param.BOUNDARY_DELTA

        if param.DIM == 3:
            if new_pos[2] < param.Z_MIN - param.BOUNDARY_DELTA:
               new_pos[2] = param.Z_MAX + param.BOUNDARY_DELTA
            elif new_pos[2] > param.Z_MAX + param.BOUNDARY_DELTA:
               new_pos[2] = param.Z_MIN - param.BOUNDARY_DELTA
        
        for i in range(param.DIM):
            self.position[i] = new_pos[i]

    
    def separation(self, neighbours: list):     # Avoidance 
        """Separate bird from neighbours that are too close."""
        if len(neighbours) == 0:
            return self.direction
        else:
            avoidance_vel = [0]*param.DIM

            for i in range(len(neighbours)):
                dist = [neighbours[i].position[j]-self.position[j] for j in range(param.DIM)]
                
                if param.DIM == 2:
                    mod_dist = math.sqrt(dist[0]**2+dist[1]**2)
                elif param.DIM == 3:
                    mod_dist = math.sqrt(dist[0]**2+dist[1]**2+dist[2]**2)

                for j in range(param.DIM):
                    avoidance_vel[j] += (param.MIN_DIST - mod_dist)*dist[j]

            for j in range(param.DIM):
                avoidance_vel[j] *= (-1/len(neighbours))

            return avoidance_vel


    def cohesion(self, birds: list):     # Centre
        """Update direction based on cohesion with other bird's positions.
        Bird will change direction to move toward the average position of all birds."""
        if len(birds) == 0:
            return self.direction
        else:
            centre = [statistics.mean([bird.position[i] for bird in birds]) for i in range(param.DIM)]
            vel_centre = [centre[i] - self.position[0] for i in range(param.DIM)]
            return vel_centre


    def alignment(self, birds: list):   # Copy
        """Update direction based on cohesion with other bird's directions (average direction)."""
        if len(birds) == 0:
            return self.direction
        else:
            avg_direction =[0]*param.DIM

            for i in range(len(birds)):
                for j in range(param.DIM):
                    avg_direction[j] += birds[i].direction[j]
    
            for j in range(param.DIM):
                avg_direction[j] = avg_direction[j]/len(birds)

            return avg_direction


    def update(self, close_neighbours, all_birds):
        """Updates direction, speed and position, considering all rules."""

        self.previous_vel = [self.speed * self.direction[i] for i in range(param.DIM)]

        vel_separation = self.separation(close_neighbours)
        vel_cohesion = self.cohesion(all_birds)
        vel_alignment = self.alignment(all_birds)

        rules_vel = [param.W_SEPARATION*vel_separation[i] + param.W_COHESION*vel_cohesion[i] + param.W_ALIGNMENT*vel_alignment[i] for i in range(param.DIM)]

        new_vel = [self.previous_vel[i]*(1-param.MU) + rules_vel[i]*param.MU for i in range(param.DIM)]

        if param.DIM == 2:
            new_speed = math.sqrt(new_vel[0]**2 + new_vel[1]**2)
        elif param.DIM == 3:
            new_speed = math.sqrt(new_vel[0]**2 + new_vel[1]**2 + new_vel[2]**2)

        self.direction = [new_vel[i]/new_speed for i in range(param.DIM)]

        if new_speed > param.MAX_VEL:
            new_speed = param.MAX_VEL
        elif new_speed < param.MIN_VEL:
            new_speed = param.MIN_VEL
        
        self.speed = new_speed

        self.updatePos(param.TIME_DELTA)



### Explain how direction of bird is defined, better
### To add obstacles and attractors: as birds, but add type parameter in __init__, to indicate if bird or obstacle or attractor
