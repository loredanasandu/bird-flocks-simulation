"""
.. module:: parameters

Parameters used while running the simulation.


.. data:: DIM: 

    (`int`) dimension of the container and simulation (2 for plane, 3 for cube).

.. data:: NUM_BIRDS: 

    (`int`) number of birds in simulation.

|

.. data:: ATTRACTION_POINTS: 

    (`list`) coordinates where attraction points will be initially located.

.. data:: REPULSION_POINTS: 

    (`list`) of coordinates where repulsion points will be initially located.

|

.. data:: W_AVOIDANCE: 

    (`float`) ratio of importance of rule of avoidance over the rest.
    
.. data:: W_CENTER: 

    (`float`) ratio of importance of rule of center over the rest.

.. data:: W_COPY: 

    (`float`) ratio of importance of rule of copy over the rest.

.. data:: W_VIEW: 

    (`float`) ratio of importance of rule of view over the rest.

.. data:: W_ATTRACTION: 

    (`float`) ratio of importance of the attraction of the poins over the rest of rules.

.. data:: W_REPULSION: 

    (`float`) ratio of importance of the repulsion of the poins over the rest of rules.

.. data:: MU: 

    (`float`) weight of new velocity vector over current one (used to smooth change of speed and direction).

|


.. data:: MIN_DIST:  

    (`int`) minimum distance that should be between birds (i.e. birds closer than this distance are too close), in pixels.

.. data:: GROUP_DIST:  

    (`int`) distance that determines the boundary of groups of birds (i.e. birds closer than this distance will be considered of the same group), in pixels.

.. data:: VIEW_DIST:  

    (`int`) distance that should be between birds regarding the view rule (i.e. birds that are in the vision area of a bird and closer than this distance are too close), in pixels.

.. data:: VIEW_ANGLE: 

    (`float`) angle that determines the vision area of a bird, in radians.

|

.. data:: MIN_DIST_ATTRACTOR: 

    (`int`) distance from which attraction points will try to escape from birds (because it will "notice" them), in pixels.

.. data:: MIN_DIST_REPULSOR:  

    (`int`) distance from which attraction points will try to go towards from birds (because it will "notice" them), in pixels.

.. data:: GROUP_DIST_REPULSOR:  

    (`int`) distance that determines which birds are withing the group boundary of the repulsion point (so it will try to go towards the center of that group), in pixels.

|

.. data:: WIDTH: 

    (`int`) width of screen, in pixels.

.. data:: HEIGHT: 

    (`int`) height of screen, in pixels.

|

.. data:: X_MIN: 

    (`int`) minimum value for x coordinate of any bird, in pixels.

.. data:: X_MAX: 

    (`int`) maximum value for x coordinate of any bird, in pixels.

.. data:: Y_MIN:  

    (`int`) minimum value for y coordinate of any bird, in pixels.

.. data:: Y_MAX:  

    (`int`) maximum value for y coordinate of any bird, in pixels.

.. data:: Z_MIN:  

    (`int`) minimum value for z coordinate of any bird, in pixels.

.. data:: Z_MAX:  

    (`int`) maximum value for z coordinate of any bird, in pixels.

|

.. data:: MIN_VEL:  

    (`int`) minimum speed of birds and points of attraction and repulsion.

.. data:: MAX_VEL:  

    (`int`) maximum speed of birds and points of attraction and repulsion.

|

.. data:: BOUNDARY_DELTA:  

    (`float`) threshold considered for the window boundary conditions.

.. data:: TIME_DELTA:  

    (`float`) small interval of time used to update position based on velocity.

.. data:: DELTA:   

    (`float`) a small arbitrary float.

|

.. data:: FPS:

    (`int`) determines the speed at which frames are updated.

|

.. data:: ROTATION:  

    (`int`) determines the speed at which cube rotates when the keys for rotation are pressed.
"""


import math


DIM = 3

NUM_BIRDS = 30

ATTRACTION_POINTS = [(200,100,200)] #[(200,200)]
REPULSION_POINTS = [(0,0,0),(100,-200,300),(400,400,400)]   #[(100,-300),(-400,400)]

W_AVOIDANCE = 10
W_CENTER = 0.1
W_COPY = 10 
W_VIEW = 1
W_ATTRACTION = 1   #0.4
W_REPULSION = 2    #1

MU = 0.05

WIDTH = 1000
HEIGHT = 1000

X_MIN = -WIDTH/2
X_MAX = -X_MIN
Y_MIN = X_MIN
Y_MAX = X_MAX
Z_MIN = X_MIN
Z_MAX = X_MAX

MIN_DIST = 30
GROUP_DIST = 200
VIEW_DIST = 50
VIEW_ANGLE = math.pi/4

MIN_DIST_ATTRACTOR = 100
MIN_DIST_REPULSOR = 100
GROUP_DIST_REPULSOR = 2000

MIN_VEL = 20
MAX_VEL = 40

BOUNDARY_DELTA = 10
TIME_DELTA = 0.1
DELTA = 0.00001

FPS = 30

ROTATION = 10
