# bird-flocks-simulation

Simulation of bird flocks, based on a mathematical model created by the same collaborators.

<img src="/figures/3d.gif" width="400" alt="Demo3D" /> <img src="/figures/2d.gif" width="350" alt="Demo2D" />

## Rules that govern the birds' motion

The behavior of bird flocks is controlled by some rules. These are the rules we've considered in our model.

* **Avoidance**: every bird tries to separate itself from birds that are too close.
* **Center**: every bird seeks cohesion with other birds' positions. That is, the bird will change its direction to move toward the average position of all birds.
* **Copy**: every bird seeks cohesion with other birds' directions. That is, the bird will change its direction to cohese with the average direction.
* **View**: a bird will move if there is another bird in its area of view.
* **Attractive objects**: there are animals and other things that attract the birds (for example, food). The presence of these objects is represented in the simulation by green circles and spheres. At the same time, these attractive objects avoid the birds.
* **Repulsive objects**: there are animals and other things that the birds try to avoid (for example, predators). The presence of these objects is represented in the simulation by red circles and spheres. At the same time, these repulsive objects will go towards the birds.

## Usage

### Installation and execution

To install the required libraries and run the simulation, execute the following commands inside the repository's directory:

```
pip install -r requirements.txt
python main.py
```

### Parameters

Parameters used to run the simulation can be changed in the parameters.py file. For example, the simulation can be runned in 2 or 3 dimensions, just by changing the value of the parameter _DIM_. Its possible values are integers: 2 or 3; and the values of the dimensions of the _ATTRACTION_POINTS_ and _REPULSION_POINTS_ have to be changed accordingly.

### Possible actions

* Use the mouse's scroll wheel to zoom in and out.
* Press the keys W, S, A and D to rotate the simulation container.
* Press R to reset the birds and the attraction and repulsion points.

## Authors
* [Anna Danot](https://github.com/Yeppo-aann)
* [Núria Fernández](https://github.com/11nunu)
* [Jan Mousavi](https://github.com/HotChilieMachine) 
* [Loredana Sandu](https://github.com/lorara11)
