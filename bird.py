"""
Here is defined the structure of a bird in the simulation.
"""

import parameters as param
import math
import statistics
import copy

class Bird:
    """The bird class"""

    def __init__(self, index: int, position: list, direction: list, speed: float, obj_type: int):
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
        self.type = obj_type    # 1 if bird, -1 if attraction point, -2 if repulsion point


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

    
    def avoidance(self, neighbours: list):
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


    def center(self, group_birds: list):
        """Update direction based on cohesion with other bird's positions.
        Bird will change direction to move toward the average position of all birds."""
        if len(group_birds) == 0:
            return self.direction
        else:
            center = [statistics.mean([bird.position[i] for bird in group_birds]) for i in range(param.DIM)]
            vel_center = [center[i] - self.position[0] for i in range(param.DIM)]
            return vel_center


    def copy(self, group_birds: list):
        """Update direction based on cohesion with other bird's directions (average direction)."""
        if len(group_birds) == 0:
            return self.direction
        else:
            avg_direction =[0]*param.DIM

            for i in range(len(group_birds)):
                for j in range(param.DIM):
                    avg_direction[j] += group_birds[i].direction[j]
    
            for j in range(param.DIM):
                avg_direction[j] = avg_direction[j]/len(group_birds)

            return avg_direction


    def view(self, group_birds: list):
        """Update direction based on the bird's view (move if there is another bird in area of view)."""

        if param.DIM == 2:
            orientation = 0
            counter = 0

            for bird in group_birds:
                if bird.index != self.index:
                    vect = [bird.position[i] - self.position[i] for i in range(param.DIM)]
                    scalar_product = sum([self.direction[i]*vect[i] for i in range(param.DIM)])
                    norm_self = math.sqrt(sum([self.direction[i]**2 for i in range(param.DIM)]))
                    norm_vect = math.sqrt(sum([vect[i]**2 for i in range(param.DIM)]))
                    norm_prod = norm_self*norm_vect
                    div = scalar_product/norm_prod
                    if div <= -1:
                        div = -1 + param.DELTA
                    elif div >= 1:
                        div = 1 - param.DELTA
                    angle = math.acos(div)

                    if abs(angle) < param.VIEW_ANGLE and norm_vect < param.VIEW_DIST:
                        orientation += (angle/abs(angle))*(param.VIEW_DIST-norm_vect)
                        counter += 1
            
            orthogonal = [self.direction[1],-self.direction[0]]
            if counter != 0:
                view_direction = [orientation*(orthogonal[i]/counter) for i in range(param.DIM)]
                return view_direction
            else:
                return copy.copy(self.direction)

        elif param.DIM == 3:
            return [0]*param.DIM

    
    def attraction(self, attraction_points):
        pass
        ### IMPLEMENTAR
        #return vel_attraction

    def repulsion(self, repulsion_points):
        pass
        ### IMPLEMENTAR
        #return vel_repulsion


    def update(self, close_neighbours, group_birds, attraction_points, repulsion_points):
        """Updates direction, speed and position, considering all rules."""

        self.previous_vel = [self.speed * self.direction[i] for i in range(param.DIM)]

        vel_avoidance = self.avoidance(close_neighbours)
        vel_center = self.center(group_birds)
        vel_copy = self.copy(group_birds)
        vel_view = self.view(group_birds)

        rules_vel = [param.W_AVOIDANCE*vel_avoidance[i] + param.W_CENTER*vel_center[i] + param.W_COPY*vel_copy[i] + param.W_VIEW*vel_view[i] for i in range(param.DIM)]

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