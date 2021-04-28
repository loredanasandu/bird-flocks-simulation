"""
Parameters used while running the simulation.

NUM_BOIDS: number of birds in simulation

W_SEPARATION: ratio of importance of rule of separation over the rest.
W_COHESION: ratio of importance of rule of cohesion over the rest.
W_ALIGNMENT: ratio of importance of rule of alignment over the rest.

WIDTH = width of screen
HEIGHT = height of screen

X_MIN: minimum value for x coordinate of any bird
X_MAX: maximum value for x coordinate of any bird
Y_MIN: minimum value for y coordinate of any bird
Y_MAX: maximum value for y coordinate of any bird
Z_MIN: minimum value for z coordinate of any bird
Z_MAX: maximum value for z coordinate of any bird

MIN_DIST: minimum distance that should be between birds 
          (i.e. birds closer than this distance are too close)

MIN_VEL: minimum speed
MAX_VEL: maximum speed
MIN_ACC: minimum acceleration
MAX_ACC: maximum acceleration

BOUNDARY_DELTA: threshold considered for the window boundary conditions
TIME_DELTA: small interval of time used to update position based on velocity
"""

DIM = 2

NUM_BIRDS = 100

W_SEPARATION = 1
W_COHESION = 1
W_ALIGNMENT = 1

WIDTH = 1000
HEIGHT = 1000

X_MIN = -WIDTH/2
X_MAX = -XMAX
Y_MIN = X_MIN
Y_MAX = X_MAX
Z_MIN = X_MAX
Z_MAX = X_MIN

MIN_DIST = 25

MIN_VEL: 1
MAX_VEL: 10
#MIN_ACC: 0
#MAX_ACC: 5

BOUNDARY_DELTA = 2.0
TIME_DELTA = 0.1