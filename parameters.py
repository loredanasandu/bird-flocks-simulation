"""
Parameters used while running the simulation.

DIM: dimension of the container and simulation (2 for plane, 3 for cube)

NUM_BIRDS: number of birds in simulation

ATTRACTION_POINTS: list of coordinates where attraction points will be located.
REPULSION_POINTS: list of coordinates where repulsion points will be located.

W_AVOIDANCE: ratio of importance of rule of avoidance over the rest.
W_CENTER: ratio of importance of rule of center over the rest.
W_COPY: ratio of importance of rule of copy over the rest.
W_VIEW: ratio of importance of rule of view over the rest.

MU: weight of new velocity vector over current one (used to smooth change of speed and direction)

WIDTH = width of screen
HEIGHT = height of screen

X_MIN: minimum value for x coordinate of any bird
X_MAX: maximum value for x coordinate of any bird
Y_MIN: minimum value for y coordinate of any bird
Y_MAX: maximum value for y coordinate of any bird
Z_MIN: minimum value for z coordinate of any bird
Z_MAX: maximum value for z coordinate of any bird

MIN_DIST: minimum distance that should be between birds (i.e. birds closer than this distance are too close)
GROUP_DIST: distance that determines the boundary of groups of birds (i.e. birds closer than this distance will be considered of the same group)
VIEW_DIST: distance that should be between birds regarding the view rule (i.e. birds that are in the vision area of a bird and closer than this distance are too close)
VIEW_ANGLE: angle that determines the vision area of a bird

MIN_VEL: minimum speed
MAX_VEL: maximum speed

BOUNDARY_DELTA: threshold considered for the window boundary conditions
TIME_DELTA: small interval of time used to update position based on velocity
DELTA: a small arbitrary float

FPS: determines the speed at which frames are updated

ROTATION: determines the speed at which cube rotates when the keys for rotation are pressed.
"""


import math


DIM = 3

NUM_BIRDS = 20

ATTRACTION_POINTS = [(0,0,0), (200,100,-300)]
REPULSION_POINTS = [(0,100,-200)]

W_AVOIDANCE = 0
W_CENTER = 0
W_COPY = 10
W_VIEW = 1

MU = 0.05

WIDTH = 1000
HEIGHT = 1000

X_MIN = -WIDTH/2
X_MAX = -X_MIN
Y_MIN = X_MIN
Y_MAX = X_MAX
Z_MIN = X_MIN
Z_MAX = X_MAX

MIN_DIST = 25
GROUP_DIST = 200
VIEW_DIST = 50
VIEW_ANGLE = math.pi/4

MIN_VEL = 20
MAX_VEL = 40

BOUNDARY_DELTA = 10
TIME_DELTA = 0.1
DELTA = 0.00001

FPS = 30

ROTATION = 10
