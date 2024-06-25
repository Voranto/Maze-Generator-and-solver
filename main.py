import time
import pygame
from sys import exit
import random
from random import choice
import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

grid_size = int(input("Type your desired grid_size: "))
time.sleep(0.5)
height = 800
width = 1600
render = True if input("Do you want the mazes rendered, this will reduce performance considerably (y/n): ") == "y" else False
time.sleep(0.5)
printinfo = True if input("Do you want the info printed in the command prompt (y/n): ") == "y" else False
time.sleep(0.5)
stats = True if input("Do you want a graph of the comparison between algorithms (y/n): ") == "y" else False
time.sleep(0.5)
if render:
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', grid_size//2)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width+2,height+2))
    pygame.display.set_caption("MAZE GENERATION")
def start():
    class Cell:
        def __init__(self,x,y):
            self.x,self.y = x,y
            self.walls= {"N":True,"S":True,"E":True,"W":True}
            self.visited = False
            self.path = []
        def draw(self):
            x ,y = self.x*grid_size,self.y*grid_size
            if self.visited:
                pygame.draw.rect(screen,"black", (x,y,grid_size,grid_size))
            if self.walls["N"]:
                pygame.draw.line(screen,"darkorange",(x,y),(x+grid_size,y),2)
            if self.walls["S"]:
                pygame.draw.line(screen,"darkorange",(x,y+grid_size),(x+grid_size,y+grid_size),2)
            if self.walls["W"]:
                pygame.draw.line(screen,"darkorange",(x,y),(x,y+grid_size),2)
            if self.walls["E"]:
                pygame.draw.line(screen,"darkorange",(x+grid_size,y),(x+grid_size,y+grid_size),2)
        def draw_curr(self):
            x ,y = self.x*grid_size,self.y*grid_size
            pygame.draw.rect(screen,"red",(x,y,grid_size,grid_size))
        def check_cell(self,x,y):
            if x < 0 or x > (width//grid_size) - 1 or y < 0 or y > (height//grid_size) - 1:
                return False
            return arr[x + y * (width//grid_size)]
        def check_neighbors(self):
            neighbors = []
            top = self.check_cell(self.x, self.y - 1)
            right = self.check_cell(self.x + 1, self.y)
            bottom = self.check_cell(self.x, self.y + 1)
            left = self.check_cell(self.x - 1, self.y)
            if top and not top.visited:
                neighbors.append(top)
            if right and not right.visited:
                neighbors.append(right)
            if bottom and not bottom.visited:
                neighbors.append(bottom)
            if left and not left.visited:
                neighbors.append(left)
            return choice(neighbors) if neighbors else False 
    def remove_walls(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['W'] = False
            next.walls['E'] = False
        elif dx == -1:
            current.walls['E'] = False
            next.walls['W'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['N'] = False
            next.walls['S'] = False
        elif dy == -1:
            current.walls['S'] = False
            next.walls['N'] = False 

    maze_start = time.time()
    arr = [Cell(col,row) for row in range(height//grid_size) for col in range(width//grid_size)]
    curr_cell = arr[0]
    stack = []
    colors = []
    #draw points
    if render:
        screen.fill("lightblue")
            
    color = 0

    #BUCLE CONSTRUIR LABERINTO
    while True:
        curr_cell.visited = True
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                    exit()

            [cell.draw() for cell in arr]
            curr_cell.draw_curr()
            for i,cell in enumerate( stack):
                pygame.draw.rect(screen,colors[i],(cell.x*grid_size,cell.y*grid_size,grid_size,grid_size))
        next = curr_cell.check_neighbors()
        if next != False:
            next.visited = True
            stack.append(curr_cell)
            colors.append((min(color, 255), 0, 103))
            color += 1
            remove_walls(curr_cell, next)
            curr_cell = next
        elif stack:
            curr_cell = stack.pop()
        else:
            break
        if render:
            pygame.display.update()



    def check_cell_solve(x,y):
        if x < 0 or x > (width//grid_size) - 1 or y < 0 or y > (height//grid_size) - 1:
            return False
        return arr[x + y * (width//grid_size)]
    maze_end = time.time()
    if printinfo:
        print("Time necessary for maze construction:"   , round(maze_end-maze_start,3), "seconds")
    start = check_cell_solve(0,random.randrange(0,height//grid_size))
    end = check_cell_solve(width//grid_size-1,random.randrange(0,height//grid_size-1))
    #end = check_cell_solve(width//grid_size-1,height//grid_size-1)
    if render:
        screen.fill("black")
        [cell.draw() for cell in arr]

    #bfs
    counter_bfs = 0
    start_time_bfs = time.time()
    stack = [start]
    visited = [start]
    predecesor = [[[arr[x + y * (width//grid_size)]] for x in range(width//grid_size)] for y in range(height//grid_size)]
    predecesor[start.y][start.x] = [start]
    while True:
        counter_bfs += 1
        if render:
            pygame.draw.rect(screen,"green", (start.x*grid_size+2,start.y*grid_size+2,grid_size-4,grid_size-4))
            pygame.draw.rect(screen,"red", (end.x*grid_size+2,end.y*grid_size+2,grid_size-4,grid_size-4))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.QUIT()
                    exit()
        curr = stack.pop(0)
        
        if curr == end:
            path = predecesor[end.y][end.x]
            break
        visited.append(curr)
        if render:
            pygame.draw.rect(screen,"blue", (curr.x*grid_size+2,curr.y*grid_size+2,grid_size-4,grid_size-4) )
        if check_cell_solve(curr.x+1 ,curr.y) and not curr.walls["E"] and check_cell_solve(curr.x+1,curr.y) not in visited:
            stack.append(check_cell_solve(curr.x+1,curr.y))
            if  predecesor[curr.y][curr.x+1]== [check_cell_solve(curr.x+1,curr.y)]:
                for val in predecesor[curr.y][curr.x]:
                    predecesor[curr.y][curr.x+1].append(val)
        if check_cell_solve(curr.x-1 ,curr.y) and not curr.walls["W"] and check_cell_solve(curr.x-1,curr.y) not in visited:
            stack.append(check_cell_solve(curr.x-1,curr.y))
            if predecesor[curr.y][curr.x-1] == [check_cell_solve(curr.x-1,curr.y)]:
                for val in predecesor[curr.y][curr.x]:
                    predecesor[curr.y][curr.x-1].append(val)
        if check_cell_solve(curr.x ,curr.y-1) and not curr.walls["N"] and check_cell_solve(curr.x,curr.y-1) not in visited:
            stack.append(check_cell_solve(curr.x,curr.y-1))
            if  predecesor[curr.y-1][curr.x]== [check_cell_solve(curr.x,curr.y-1)]:
                for val in predecesor[curr.y][curr.x]:
                    predecesor[curr.y-1][curr.x].append(val)
        if check_cell_solve(curr.x ,curr.y+1) and not curr.walls["S"] and check_cell_solve(curr.x,curr.y+1) not in visited:
            stack.append(check_cell_solve(curr.x,curr.y+1))
            if  predecesor[curr.y+1][curr.x] == [check_cell_solve(curr.x,curr.y+1)]:
                for val in predecesor[curr.y][curr.x]:
                    predecesor[curr.y+1][curr.x].append(val)
        if render:
            pygame.display.update()
        
        
        
    path = predecesor[end.y][end.x]
    if render:
        screen.fill("black")
        [cell.draw() for cell in arr]
    end_time_bfs = time.time()
    if printinfo:
        print("Time required for BFS: ", round(end_time_bfs-start_time_bfs,3)," seconds")
        print("BFS iterations: ", counter_bfs)
    if render:
        for i in range(1,len(path)):
                pygame.draw.line(screen,"blue",(path[i-1].x*grid_size+grid_size//2,path[i-1].y*grid_size+grid_size//2),(path[i].x*grid_size+grid_size//2,path[i].y*grid_size+grid_size//2),10)
                pygame.draw.circle(screen,"blue",(path[i-1].x*grid_size+grid_size//2,path[i-1].y*grid_size+grid_size//2),3)
        pygame.draw.rect(screen,"green", (start.x*grid_size+2,start.y*grid_size+2,grid_size-4,grid_size-4))
        pygame.draw.rect(screen,"red", (end.x*grid_size+2,end.y*grid_size+2,grid_size-4,grid_size-4))
        pygame.display.update()


    #A-star
    #screen reset
    if render:
        screen.fill("black")
        [cell.draw() for cell in arr]

    def h(x,y):
        #return math.sqrt((x - end.x)**2 + (y - end.y)**2)
        return abs (x - end.x) + abs (y - end.y)

    def f(h,depth):
        return h*2 + depth


    visited_depth = set([(start,0)])
    visited = set([start])
    start.path = [start]
    counter_astar = 0
    astar_start = time.time()
    g_score = {start:0}
    came_from = {}
    if render:
        pygame.draw.rect(screen,"green", (start.x*grid_size+2,start.y*grid_size+2,grid_size-4,grid_size-4))
    new_node = start
    vecinos_heap = []
    heapq.heappush(vecinos_heap, (f(h(start.x, start.y), 0), 0, (start.x, start.y), start))

    while True:
        counter_astar += 1
        
        x, y = new_node.x, new_node.y
        
        
        for direction, (dx, dy) in [("E", (1, 0)), ("W", (-1, 0)), ("N", (0, -1)), ("S", (0, 1))]:
            if not new_node.walls[direction]:
                neighbor = check_cell_solve(x + dx, y + dy)
                if neighbor not in visited:
                    tentative_g_score = g_score[new_node] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = new_node
                        g_score[neighbor] = tentative_g_score
                        heapq.heappush(vecinos_heap, (f(h(x + dx, y + dy), tentative_g_score), tentative_g_score, (x + dx, y + dy), neighbor))
                    if render:
                        pygame.draw.rect(screen, "lightblue", (neighbor.x * grid_size + 2, neighbor.y * grid_size + 2, grid_size - 4, grid_size - 4))

        temp = new_node
        # Extraer el vecino con el menor f-score
        _, new_depth, _, new_node = heapq.heappop(vecinos_heap)
        new_node.path.append(new_node)
        if  new_node.path == []:
            for camino in temp.path:
                if camino not in new_node.path:
                    new_node.path.append(camino)
            
        if new_node == end:
            break
        if render:
            pygame.draw.rect(screen, "lightblue", (new_node.x * grid_size + 2, new_node.y * grid_size + 2, grid_size - 4, grid_size - 4))

        visited_depth.add((new_node, new_depth))
        visited.add(new_node)
        if render:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()


    astart_end = time.time()
    if printinfo:
        print("A star took: ", round(astart_end - astar_start,3), "seconds")
        print("A star iterations: ", counter_astar)
    if render:
        screen.fill("black")
        [cell.draw() for cell in arr]
        for i in range(1,len(end.path)):
            pygame.draw.line(screen,"blue",(end.path[i-1].x*grid_size+grid_size//2,end.path[i-1].y*grid_size+grid_size//2),(end.path[i].x*grid_size+grid_size//2,end.path[i].y*grid_size+grid_size//2),10)
            pygame.draw.circle(screen,"blue",(end.path[i-1].x*grid_size+grid_size//2,end.path[i-1].y*grid_size+grid_size//2),3)
        pygame.draw.rect(screen,"green", (start.x*grid_size+2,start.y*grid_size+2,grid_size-4,grid_size-4))
        pygame.draw.rect(screen,"red", (end.x*grid_size+2,end.y*grid_size+2,grid_size-4,grid_size-4))
        pygame.display.update()
    return counter_bfs,counter_astar, end_time_bfs-start_time_bfs,astart_end-astar_start,maze_end-maze_start


iterations = int(input("Number of iterations: "))
if stats:
    bfs_times = []
    astar_times = []
    x_axis = []
    bfs_iterations = []
    astar_iterations = []
    maze_times = []
    fig, axs = plt.subplots(2)
    fig.suptitle("Statistics of maze building and solving algorithm")
    graph1, = axs[0].plot(x_axis,bfs_times,color = 'g',label = "BFS time")
    graph2, = axs[0].plot(x_axis,astar_times,color = 'r',label = "A* time")
    graph3, = axs[1].plot(x_axis,bfs_iterations,color = 'g',label = "BFS squares checked")
    graph4, = axs[1].plot(x_axis,astar_iterations,color = 'r',label = "A* squares checked")
    axs[0].legend()
    axs[1].legend()
    def update(frame):
        bfs_c, astar_c, bfs_time, astar_time, maze_time = start()
        x_axis.append(frame)
        bfs_times.append(bfs_time)
        astar_times.append(astar_time)
        bfs_iterations.append(bfs_c)
        astar_iterations.append(astar_c)
        graph1.set_xdata(x_axis)
        graph1.set_ydata(bfs_times)
        graph2.set_xdata(x_axis)
        graph2.set_ydata(astar_times)
        graph3.set_xdata(x_axis)
        graph3.set_ydata(bfs_iterations)
        graph4.set_xdata(x_axis)
        graph4.set_ydata(astar_iterations)
        axs[0].relim()
        axs[0].autoscale_view()
        axs[1].relim()
        axs[1].autoscale_view()
        

    anim = FuncAnimation(fig, update, frames=range(iterations), repeat=False)

    plt.show()
else:
    for i in range(iterations):
        start()     


    
