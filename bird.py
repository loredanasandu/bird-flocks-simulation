"""
.. module:: bird

Here is defined the structure of a bird in the simulation.
"""

import parameters as param
import math
import statistics
import copy


class Bird:
    """
    The class that represents a bird.

    :param index: index that identifies bird.
    :type index: int
    :param position: coordinates (x,y,z) of bird.
    :type position: list
    :param direction: direction of bird's velocity vector with coordinates (x,y,z), as a unit vector.
    :type direction: list
    :param speed: module of bird's velocity vector.
    :type speed: float
    :param type: the type of object that the instance represents. Value 1 for bird, -1 for attraction point, -2 for repulsion point.
    :type type: int

    |
    """

    def __init__(self, index: int, position: list, direction: list, speed: float, type: int):
        """
        Constructor for the bird class.

        |
        """
    
        self.index = index
        self.position = position
        self.direction = direction
        self.speed = speed
        self.previous_vel = 0
        self.type = type    # 1 if bird, -1 if attraction point, -2 if repulsion point


    def updatePos(self, diff_time):
        """
        Update bird's position using speed and direction.
        Takes into consideration boundary conditions.

        :param diff_time: small interval of time used to update position based on velocity.
        :type diff_time: float

        |
        """

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
        """
        Separate bird from neighbours that are too close.

        :param neighbours: birds that are closer to the bird than the minimum distance (see :py:data:`MIN_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type neighbours: list
        :return: velocity vector that responds to the Avoidance rule.
        :rtype: list

        |
        """

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
                    
                dist = [dist[i]/mod_dist for i in range(param.DIM)]

                for j in range(param.DIM):
                    avoidance_vel[j] += (param.MIN_DIST - mod_dist)*dist[j]

            for j in range(param.DIM):
                avoidance_vel[j] *= (-1/len(neighbours))

            return avoidance_vel


    def center(self, group_birds: list):
        """
        Seek cohesion with other bird's positions.
        Bird will change direction to move toward the average position of all birds.

        :param group_birds: birds that are closer to the bird than the group boundary distance (see :py:data:`GROUP_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type group_birds: list
        :return: velocity vector that responds to the Center rule.
        :rtype: list

        |
        """

        if len(group_birds) == 0:
            return self.direction
        else:
            center = [statistics.mean([bird.position[i] for bird in group_birds]) for i in range(param.DIM)]
            vel_center = [center[i] - self.position[0] for i in range(param.DIM)]
            return vel_center


    def copy(self, group_birds: list):
        """
        Seek cohesion with other bird's directions (average direction).

        :param group_birds: birds that are closer to the bird than the group boundary distance (see :py:data:`GROUP_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type group_birds: list
        :return: velocity vector that responds to the Copy rule.
        :rtype: list

        |
        """

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
        """
        Move if there is another bird in area of view.

        :param group_birds: birds that are closer to the bird than the group boundary distance (see :py:data:`GROUP_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type group_birds: list
        :return: velocity vector that responds to the View rule.
        :rtype: list

        |
        """

        orientation = 0
        counter = 0
        view_vel = [0]*param.DIM

        for bird in group_birds:
            if bird.index != self.index:
                vect_dist = [bird.position[i] - self.position[i] for i in range(param.DIM)]
                scalar_product = sum([self.direction[i]*vect_dist[i] for i in range(param.DIM)])
                norm_self = math.sqrt(sum([self.direction[i]**2 for i in range(param.DIM)]))
                norm_dist = math.sqrt(sum([vect_dist[i]**2 for i in range(param.DIM)]))
                norm_prod = norm_self*norm_dist
                div = scalar_product/norm_prod
                if div <= -1:
                    div = -1 + param.DELTA
                elif div >= 1:
                    div = 1 - param.DELTA
                angle = math.acos(div)

                if abs(angle) < param.VIEW_ANGLE and norm_dist < param.VIEW_DIST:

                    if param.DIM == 2:
                        orientation += (angle/abs(angle))*(param.VIEW_DIST-norm_dist)

                    elif param.DIM == 3:
                        vect_dist = [(vect_dist[i]*norm_self) / (norm_dist*math.cos(angle)) for i in range(param.DIM)]
                        
                        view_vel_bird = [self.direction[i] - vect_dist[i] for i in range(param.DIM)]
                        norm_view_vel_bird = math.sqrt(sum([view_vel_bird[i]**2 for i in range(param.DIM)]))

                        view_vel = [view_vel[i] + ((view_vel_bird[i]/norm_view_vel_bird) * (param.VIEW_DIST - norm_view_vel_bird)) for i in range(param.DIM)]

                    counter += 1

        if counter != 0:

            if param.DIM == 2:
                orthogonal = [self.direction[1],-self.direction[0]]
                view_vel = [orientation*(orthogonal[i]/counter) for i in range(param.DIM)]
                return view_vel
            
            elif param.DIM == 3:
                view_vel = [view_vel[i]/counter for i in range(param.DIM)]
                return view_vel

        else:
            return copy.copy(self.direction)
            
                        
    def attraction(self, attraction_points):
        """
        Go towards attraction points.

        :param attraction_points: list of coordinates of the attraction points (see :py:data:`ATTRACTION_POINTS` in :py:mod:`parameters`).
        :type attraction_points: list
        :return: velocity vector that responds to the attraction of the corresponding points.
        :rtype: list

        |
        """

        vel_attraction = [0]*param.DIM
        counter = 0

        for point in attraction_points:
            dist = [point.position[i] - self.position[i] for i in range(param.DIM)]

            vel_attraction = [vel_attraction[i] + dist[i] for i in range(param.DIM)]
            counter += 1

        if counter != 0:
            vel_attraction = [vel_attraction[i] / counter for i in range(param.DIM)]
            return vel_attraction

        else:
            return copy.copy(self.direction)


    def repulsion(self, repulsion_points):
        """
        Go towards repulsion points.

        :param repulsion_points: list of coordinates of the repulsion points (see :py:data:`REPULSION_POINTS` in :py:mod:`parameters`).
        :type repulsion_points: list
        :return: velocity vector that responds to the repulsion of the corresponding points.
        :rtype: list

        |
        """

        vel_repulsion = [0]*param.DIM
        counter = 0

        for point in repulsion_points:
            dist = [point.position[i] - self.position[i] for i in range(param.DIM)]

            vel_repulsion = [vel_repulsion[i] + dist[i] for i in range(param.DIM)]
            counter += 1

        if counter != 0:
            vel_repulsion = [-vel_repulsion[i] / counter for i in range(param.DIM)]
            return vel_repulsion
        else:
            return copy.copy(self.direction)


    def update(self, close_neighbours, group_birds, attraction_points, repulsion_points):
        """
        Updates direction, speed and position of bird, considering all rules, and the attraction and repulsion points.

        :param close_neighbours: birds that are closer to the bird than the minimum distance (see :py:data:`MIN_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type close_neighbours: list
        :param group_birds: birds that are closer to the bird than the group boundary distance (see :py:data:`GROUP_DIST` in :py:mod:`parameters`). Birds are represented as instances of the :class:`bird.Bird` class.
        :type group_birds: list
        :param attraction_points: list of coordinates of the attraction points (see :py:data:`ATTRACTION_POINTS` in :py:mod:`parameters`).
        :type attraction_points: list
        :param repulsion_points: list of coordinates of the repulsion points (see :py:data:`REPULSION_POINTS` in :py:mod:`parameters`).
        :type repulsion_points: list

        |
        """

        self.previous_vel = [self.speed * self.direction[i] for i in range(param.DIM)]

        vel_avoidance = self.avoidance(close_neighbours)
        vel_center = self.center(group_birds)
        vel_copy = self.copy(group_birds)
        vel_view = self.view(group_birds)
        vel_attraction = self.attraction(attraction_points)
        vel_repulsion = self.repulsion(repulsion_points)

        rules_vel = [param.W_AVOIDANCE*vel_avoidance[i] + param.W_CENTER*vel_center[i] + param.W_COPY*vel_copy[i] + param.W_VIEW*vel_view[i] \
                    + param.W_ATTRACTION*vel_attraction[i] + param.W_REPULSION*vel_repulsion[i] for i in range(param.DIM)]

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


    def updateAttractor(self, all_birds):
        """
        Updates direction, speed and position of the attractor points. 
        They will avoid the birds that are closer than a minimum distance (see :py:data:`MIN_DIST_ATTRACTOR` in :py:mod:`parameters`).

        :param all_birds: all the birds in the simulation, represented as instances of the :class:`bird.Bird` class.
        :type all_birds: list

        |
        """

        self.previous_vel = [self.speed * self.direction[i] for i in range(param.DIM)]

        close_birds = []

        for bird in all_birds:
            if param.DIM == 2:
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2)<param.MIN_DIST_ATTRACTOR:
                    close_birds.append(bird)
            elif param.DIM == 3:
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2+(self.position[2]-bird.position[2])**2)<param.MIN_DIST_ATTRACTOR:
                    close_birds.append(bird)

        vel_not_avoidance = self.avoidance(close_birds)
        vel_avoidance = [-vel_not_avoidance[i] for i in range(param.DIM)]
        
        rules_vel = [param.W_AVOIDANCE*vel_avoidance[i] for i in range(param.DIM)]
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

    
    def updateRepulsor(self, all_birds):
        """
        Updates direction, speed and position of the repulsion points. 
        They will go towards the birds that are closer than a minimum distance (see :py:data:`MIN_DIST_REPULSOR` in :py:mod:`parameters`).
        They will also go towards the center of the group of birds that are closer than a group boundary distance (see :py:data:`GROUP_DIST_REPULSOR` in :py:mod:`parameters`).

        :param all_birds: all the birds in the simulation, represented as instances of the :class:`bird.Bird` class.
        :type all_birds: list

        |
        """

        self.previous_vel = [self.speed * self.direction[i] for i in range(param.DIM)]

        close_birds = []
        group_birds = []

        for bird in all_birds:
            if param.DIM == 2:
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2)<param.MIN_DIST_REPULSOR:
                    close_birds.append(bird)
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2)<param.GROUP_DIST_REPULSOR:
                    group_birds.append(bird)
            elif param.DIM == 3:
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2+(self.position[2]-bird.position[2])**2)<param.MIN_DIST_ATTRACTOR:
                    close_birds.append(bird)
                if math.sqrt((self.position[0]-bird.position[0])**2+(self.position[1]-bird.position[1])**2+(self.position[2]-bird.position[2])**2)<param.GROUP_DIST_REPULSOR:
                    group_birds.append(bird)

        vel_not_avoidance = self.avoidance(close_birds)
        vel_center = self.center(group_birds)
        
        rules_vel = [param.W_AVOIDANCE*vel_not_avoidance[i] + param.W_CENTER*vel_center[i] for i in range(param.DIM)]
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
