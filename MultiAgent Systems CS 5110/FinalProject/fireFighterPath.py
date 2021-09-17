from pygame.locals import *
import pygame, sys, random
from os import path
import heapq
vec = pygame.math.Vector2
import csv
import datetime
#import numpy as np

#constants representing colours

BLACK = (0,   0,   0  )
BROWN = (153, 76,  0  )
GREEN = (0,   255, 0  )
BLUE  = (0,   0,   255)
WHITE = (255, 255, 255)
MEDGRAY = (75, 75, 75)

#constants representing the different resources

DIRT  = 0
GRASS = 1
TREE = 2
FIRE  = 3
BURNT = 4
FIREMEN = 5 #= pygame.image.load('img/player1.png')
TURN = 6

#a dictionary linking resources to textures
textures =   {
                DIRT   : pygame.image.load('img/dirt1.png'),
                GRASS  : pygame.image.load('img/grass1.png'),
                TREE  : pygame.image.load('img/tree2.png'),
                FIRE   : pygame.image.load('img/treeFire.png'),
                BURNT   : pygame.image.load('img/deadTree1.png'),
                FIREMEN : pygame.image.load('img/player1.png'),
                TURN : pygame.image.load('img/clock1.png'),
            }

statInfo =   {

                DIRT   : 0,
                GRASS  : 0,
                TREE  : 0,
                FIRE   : 0,
                BURNT   :0,
                FIREMEN   :0,
                TURN : 0
            }



#GLO
TILESIZE  = 20
MAPWIDTH  = 80 #30
MAPHEIGHT = 50 #20
TOTAL_MAP_SIZE = MAPWIDTH * MAPHEIGHT
NUM_PLAYERS = 50
FPS = 30
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + 50))

#a list of resources
resources = [DIRT,GRASS,TREE,FIRE,BURNT,FIREMEN ,TURN]
#use list comprehension to create our tilemap
#[y][x]
tilemap = [ [DIRT for w in range(MAPWIDTH)] for h in range(MAPHEIGHT) ]

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
        # comment/uncomment this for diagonals:
        self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

class PriorityQueue:
    def __init__(self):
        self.nodes = []

    def put(self, node, cost):
        heapq.heappush(self.nodes, (cost, node))

    def get(self):
        return heapq.heappop(self.nodes)[1]

    def empty(self):
        return len(self.nodes) == 0

def vec2int(v):
    return (int(v.x), int(v.y))

def heuristic(a, b):
    # return abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2
    return (abs(a.x - b.x) + abs(a.y - b.y)) * 10

def a_star_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        # if current == end:
        #     break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost + heuristic(end, vec(next))
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path, cost

class WeightedGrid(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        if (vec(to_node) - vec(from_node)).length_squared() == 1:
            return self.weights.get(to_node, 1) + 10
        else:
            return self.weights.get(to_node, 1) + 14

def dijkstra_search(graph, start, end):
    frontier = PriorityQueue()
    frontier.put(vec2int(start), 0)
    path = {}
    cost = {}
    path[vec2int(start)] = None
    cost[vec2int(start)] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            break
        for next in graph.find_neighbors(vec(current)):
            next = vec2int(next)
            next_cost = cost[current] + graph.cost(current, next)
            if next not in cost or next_cost < cost[next]:
                cost[next] = next_cost
                priority = next_cost
                frontier.put(next, priority)
                path[next] = vec(current) - vec(next)
    return path, cost

def closest_node( xy, nodes):
      nodes = np.asarray(xy)
      deltas = nodes - xy
      dist_2 = np.einsum('ij,ij->i', deltas, deltas)
      return np.argmin(dist_2)


#import scipy.spatial


# def get_closest_point(point,fire_list):
#     #https: // stackoverflow.com / q / 10818546
#     # # Shoe-horn existing data for entry into KDTree routines
#     # # Create some dummy data
#     y_array = np.random.random(10000).reshape(100, 100)
#     x_array = np.random.random(10000).reshape(100, 100)

#     points = np.random.random(10000).reshape(2, 5000)
#     combined_x_y_arrays = np.dstack([y_array.ravel(), x_array.ravel()])[0]

#     points = np.array((fire_list))
#     combined_x_y_arrays = np.array(list(fire_list)) #    combined_x_y_arrays = np.dstack(fire_list)

#     #points_list = list(points.transpose())

#     def do_kdtree(combined_x_y_arrays, points):
#         mytree = scipy.spatial.cKDTree(combined_x_y_arrays)
#         dist, indexes = mytree.query(points)
#         return indexes

#     #results2 = do_kdtree(combined_x_y_arrays, points_list)
#     results2 = do_kdtree(combined_x_y_arrays, list(points))

def any_fule(playerPos):
    directions = ["UP", "UP_Left", "UP_Right", "DOWN", "DOWN_Left", "DOWN_Right", "LEFT", "RIGHT"]
    random.shuffle(directions)
    for i in range(len(directions)):
        move = directions[i]
        if move == "RIGHT" and playerPos[0] < MAPWIDTH - 1:
            if tilemap[playerPos[1]][playerPos[0] + 1] == TREE or \
                    tilemap[playerPos[1]][playerPos[0] + 1] == GRASS:
                tilemap[playerPos[1]][playerPos[0] + 1] = DIRT
                playerPos = [playerPos[0] + 1, playerPos[1]]
                return True
            else:
                continue

        if move == "LEFT" and playerPos[0] > 0:
            if tilemap[playerPos[1]][playerPos[0] - 1] == TREE or\
                    tilemap[playerPos[1]][playerPos[0] -1] == GRASS:
                tilemap[playerPos[1]][playerPos[0] - 1] = DIRT
                playerPos = [playerPos[0] - 1, playerPos[1]]
                return True
            else:
                continue

        if move == "UP" and playerPos[1] > 0:
            if tilemap[playerPos[1]-1][playerPos[0]] == TREE or tilemap[playerPos[1]-1][playerPos[0]] == GRASS:
                tilemap[playerPos[1]-1][playerPos[0]] = DIRT
                playerPos = [playerPos[0], playerPos[1]-1]
                return True
            else:
                continue
        if move == "UP_Left" and playerPos[1] > 0 and playerPos[0] > 0:
            if tilemap[playerPos[1]-1][playerPos[0]-1] == TREE or \
                    tilemap[playerPos[1]-1][playerPos[0]-1] == GRASS:
                tilemap[playerPos[1]-1][playerPos[0]-1] = DIRT
                playerPos = [playerPos[0]-1, playerPos[1]-1]
                return True
            else:
                continue
        if move == "UP_Right" and playerPos[1] > 0 and playerPos[0] < MAPWIDTH - 1:
            if tilemap[playerPos[1]-1][playerPos[0]+1] == TREE or \
                    tilemap[playerPos[1]-1][playerPos[0]+1] == GRASS:
                tilemap[playerPos[1]-1][playerPos[0]+1] = DIRT
                playerPos = [playerPos[0]+1, playerPos[1]-1]
                return True
            else:
                continue
        if move == "DOWN" and playerPos[1] < MAPHEIGHT - 1:
            if tilemap[playerPos[1]+1][playerPos[0]] == TREE or \
                    tilemap[playerPos[1]+1][playerPos[0]] == GRASS:
                tilemap[playerPos[1]+1][playerPos[0]] = DIRT
                playerPos = [playerPos[0], playerPos[1]+1]
                return True
            else:
                continue
        if move == "DOWN_Left" and playerPos[1] < MAPHEIGHT - 1 and playerPos[0] > 0:
            if tilemap[playerPos[1]+1][playerPos[0]-1] == TREE or \
                    tilemap[playerPos[1]+1][playerPos[0]-1] == GRASS:
                tilemap[playerPos[1]+1][playerPos[0]-1] = DIRT
                playerPos = [playerPos[0]-1, playerPos[1]+1]
                return True
            else:
                continue
        if move == "DOWN_Right" and playerPos[1] < MAPHEIGHT - 1 and playerPos[0] < MAPWIDTH - 1:
            if tilemap[playerPos[1]+1][playerPos[0]+1] == TREE or \
                    tilemap[playerPos[1]+1][playerPos[0]+1] == GRASS:
                tilemap[playerPos[1]+1][playerPos[0]+1] = DIRT
                playerPos = [playerPos[0]+1, playerPos[1]+1]
                return True
            else:
                continue
    else:
        return False



class FireMan():
    def __init__(self,startPos ):
        self.cerPos = startPos
        self.img = pygame.image.load('img/player1.png')
        self.nextDest =[0,0]

    def pathBasic1( self,fire_list):
        #Based on other agents/fire move
        xy = self.cerPos
        #closest_node(xy, fire_list)
        get_closest_point(xy, fire_list)

    def pathBasic1( self):
        #Based on other agents/fire move
        playerPos = self.cerPos
        # Starting Simple 

        #Fire Fighter Makes a Chois based on a List of Prioretys
        #1 Stay alive
        #2 Help anyone who could die
        #3 Move to Stop Fire
        #4 dig a line
            #4.1 if on dirt then 
        #5 Keep formation /Say togethoer
        #if the right arrow is pressed
        if tilemap[playerPos[1]][playerPos[0]] ==FIRE:
            return False

        directions = ["UP","UP_Left","UP_Right","DOWN","DOWN_Left","DOWN_Right","LEFT","RIGHT"]
        random.shuffle(directions)
        for i in range(len(directions)):
            move = directions[i]
            if move == "RIGHT" and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[0] += 1
                return True
            if move == "LEFT" and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[0] -= 1
                return True
            if move == "UP" and playerPos[1] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[1] -= 1
                return True
            if move == "UP_Left" and playerPos[1] > 0 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[1] -= 1
                playerPos[0] -= 1
                return True
            if move == "UP_Right" and playerPos[1] > 0 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[1] -= 1
                playerPos[0] += 1
                return True
            if move == "DOWN" and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]]=DIRT
                    continue
                playerPos[1] += 1
                return True
            if move == "DOWN_Left" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[1] += 1
                playerPos[0] -= 1
                return True
            if move == "DOWN_Right" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    continue
                playerPos[1] += 1
                playerPos[0] += 1
                return True
        else:
            return False

    def pathBasic2( self):
        #Based on other agents/fire move
        playerPos = self.cerPos
        # Starting Simple 

        #Fire Fighter Makes a Chois based on a List of Prioretys
        #1 Stay alive
        #2 Help anyone who could die
        #3 Move to Stop Fire
        #4 dig a line
            #4.1 if on dirt then 
        #5 Keep formation /Say togethoer
        #if the right arrow is pressed
        if tilemap[playerPos[1]][playerPos[0]] ==FIRE:
            return False

        directions = ["UP","UP_Left","UP_Right","DOWN","DOWN_Left","DOWN_Right","LEFT","RIGHT"]
        random.shuffle(directions)
        for i in range(len(directions)):
            move = directions[i]
            if move == "RIGHT" and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[0] += 1
                return True
            if move == "LEFT" and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[0] -= 1
                return True
            if move == "UP" and playerPos[1] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                return True
            if move == "UP_Left" and playerPos[1] > 0 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                playerPos[0] -= 1
                return True
            if move == "UP_Right" and playerPos[1] > 0 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                playerPos[0] += 1
                return True
            if move == "DOWN" and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]]=DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                return True
            if move == "DOWN_Left" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]-1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                playerPos[0] -= 1
                return True
            if move == "DOWN_Right" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]+1] ==FIRE:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                playerPos[0] += 1
                return True
        else:
            return False
    
    def pathBasic3( self):
        #Based on other agents/fire move
        playerPos = self.cerPos
        # Starting Simple 

        #Fire Fighter Makes a Chois based on a List of Prioretys
        #1 Stay alive
        #2 Help anyone who could die
        #3 Move to Stop Fire
        #4 dig a line
            #4.1 if on dirt then 
        #5 Keep formation /Say togethoer
        #if the right arrow is pressed
        if tilemap[playerPos[1]][playerPos[0]] ==FIRE:
            return False

        directions = ["UP","UP_Left","UP_Right","DOWN","DOWN_Left","DOWN_Right","LEFT","RIGHT"]
        random.shuffle(directions)
        for i in range(len(directions)):
            move = directions[i]
            if move == "RIGHT" and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]+1] ==FIRE or tilemap[playerPos[1]][playerPos[0]+1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[0] += 1
                return True
            if move == "LEFT" and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]][playerPos[0]-1] ==FIRE or tilemap[playerPos[1]][playerPos[0]-1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[0] -= 1
                return True
            if move == "UP" and playerPos[1] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]] ==FIRE or tilemap[playerPos[1]-1][playerPos[0]] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                return True
            if move == "UP_Left" and playerPos[1] > 0 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]-1] ==FIRE or tilemap[playerPos[1]-1][playerPos[0]-1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                playerPos[0] -= 1
                return True
            if move == "UP_Right" and playerPos[1] > 0 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]-1][playerPos[0]+1] ==FIRE or tilemap[playerPos[1]-1][playerPos[0]+1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] -= 1
                playerPos[0] += 1
                return True
            if move == "DOWN" and playerPos[1] < MAPHEIGHT -1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]] ==FIRE or tilemap[playerPos[1]+1][playerPos[0]] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]]=DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                return True
            if move == "DOWN_Left" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] > 0:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]-1] ==FIRE or tilemap[playerPos[1]+1][playerPos[0]-1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                playerPos[0] -= 1
                return True
            if move == "DOWN_Right" and playerPos[1] < MAPHEIGHT -1 and playerPos[0] < MAPWIDTH - 1:
                #change the player's x position
                if tilemap[playerPos[1]+1][playerPos[0]+1] ==FIRE or tilemap[playerPos[1]+1][playerPos[0]+1] == BURNT:
                    if tilemap[playerPos[1]][playerPos[0]] ==TREE or tilemap[playerPos[1]][playerPos[0]] ==GRASS:
                        tilemap[playerPos[1]][playerPos[0]] = DIRT
                    if any_fule(playerPos):
                        return True
                    continue
                playerPos[1] += 1
                playerPos[0] += 1
                return True
        else:
            return False

    def setFireFighterPath( playerPos):
        move = "DOWN"

        #if the right arrow is pressed
        if move == "RIGHT" and playerPos[0] < MAPWIDTH - 1:
            #change the player's x position
            playerPos[0] += 1
        if move == "LEFT" and playerPos[0] > 0:
            #change the player's x position
            playerPos[0] -= 1
        if move == "UP" and playerPos[1] > 0:
            #change the player's x position
            playerPos[1] -= 1
        if move == "DOWN" and playerPos[1] < MAPHEIGHT -1:
            #change the player's x position
            playerPos[1] += 1



def GameOver(statInfo,resources,ticks,FIREMEN_Alive,tilemap):
    endMess = pygame.image.load('img/end.png')
    messg =[0,0]
    DISPLAYSURF.blit(endMess,(messg[0]*TILESIZE,messg[1]*TILESIZE))
    pygame.display.update()

    statInfo = statInfo.fromkeys(statInfo,0)
    
    #loop through each row
    for row in range(MAPHEIGHT):
        #loop through each column in the row
        for column in range(MAPWIDTH):
            #draw the resource at that position in the tilemap, using the correct image
            statInfo[tilemap[row][column]] +=1
 
    
    with open('DATA.csv', 'a') as csvFile:
        # writer = csv.writer(csvFile, delimiter=',')
        # for line in resources:
        #     writer.writerow(line)
        writer = csv.writer(csvFile,delimiter=',')
        #writer.writerow(" ")
        #writer.writerow(["Algorthom: pathBasic() ",str(datetime.datetime.today())])
        #writer.writerow(["DIRT","GRASS","TREE","FIRE","BURNT","FIREMEN","TURN"])
        writer.writerow([
             str(statInfo[DIRT]),
             str(statInfo[GRASS]),
             str(statInfo[TREE]),
             str(statInfo[FIRE]),
             str(statInfo[BURNT]),
             str(FIREMEN_Alive),
             str(ticks)] )
    
    csvFile.close()

    pygame.event.clear()
    pygame.event.wait()
    

