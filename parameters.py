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

BOUNDARY_DELTA: threshold considered for the window boundary conditions
TIME_DELTA: small interval of time used to update position based on velocity
"""

DIM = 3

NUM_BIRDS = 20

W_SEPARATION = 0.1
W_COHESION = 0
W_ALIGNMENT = 0.9

### EXPLICAR
MU = 0.01

WIDTH = 1000
HEIGHT = 1000

X_MIN = -WIDTH/2
X_MAX = -X_MIN
Y_MIN = X_MIN
Y_MAX = X_MAX
Z_MIN = X_MIN
Z_MAX = X_MAX

MIN_DIST = 100

MIN_VEL = 20
MAX_VEL = 50

BOUNDARY_DELTA = 10
TIME_DELTA = 0.1

FPS = 30

ROTATION = 10