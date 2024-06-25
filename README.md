# Maze-Generator-and-solver
Algorithm to build mazes using the randomized DFS, and a solving using both dijkstra and A* for comparison

# USE
Latest Python version required: https://www.python.org/downloads/

How to install libraries required
'''
pip install pygame
pip install matplotlib
'''

When asked from grid size it refers to the size of each pixel making up the maze. A value between 10 and 100 is recommended. To reduce offcentered mazes try to use numbers divisible both by 800 and 1600 (which are the dimensions of the pygame screen).

The rest of the inputs are pretty self explanatory

Rendering the actual pygame maze does reduce significantly performance, using a grid size lower than 50 while rendering the screen is not recommended. 
