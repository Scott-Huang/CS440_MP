from collections import deque

# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Kelvin Ma (kelvinm2@illinois.edu) on 01/24/2021

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
# Search should return the path.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,astar,astar_multi,fast)


class Node:
    def __init__(self, position=(0,0), cost=0, goals=None, pastNode=None):
        self.position = position
        self.parent = pastNode
        self.cost = cost
        self.goals = goals
    def update(self, pastNode, cost):
        self.parent = pastNode
        self.cost = cost
def find(list, position, goals):
    for i in list[position]:
        if i.goals == goals:
            return i
    return None

def bfs(maze):
    """
    Runs BFS for part 1 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    explored = []
    queue = deque()
    target = maze.waypoints[0]

    queue.append(Node(maze.start, 0))
    explored.append(maze.start)
    while queue: #whle the queue is not empty, which means there are paths going to be explored
        node = queue[0]
        queue.popleft()
        if node.position == target:
            break

        neighbors = maze.neighbors(node.position[0], node.position[1])
        for neighbor in neighbors:
            if maze.navigable(neighbor[0], neighbor[1]) and neighbor not in explored:
                queue.append(Node(neighbor, 0, None, node))
                explored.append(neighbor)

    ret = []
    while node != None:
        ret.append(node.position)
        node = node.parent
    ret.reverse()
    return ret

def shorter(x, y, gh): # return true if x is shorter than y heriustically
    if gh(x) < gh(y):
        return True
    return False
def insert(x, list, gh):
    for i in range(len(list)):
        if shorter(x, list[i], gh):
            list.insert(i, x)
            return
    list.append(x)

def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """

    explored = []
    states = {} # {postion: (parent, cost)}
    queue = []
    target = maze.waypoints[0]
    def h(x):
        return abs(x[0]-target[0]) + abs(x[1]-target[1])
    def gh(x):
        return h(x) + states[x][1]

    queue.append(maze.start)
    states[maze.start] = (None, 0)
    explored.append(maze.start)

    while queue:
        node = queue[0]
        queue.pop(0)
        if node == target:
            break

        neighbors = maze.neighbors(node[0], node[1])
        parent, cost = states[node]
        cost += 1
        for neighbor in neighbors:
            if maze.navigable(neighbor[0], neighbor[1]):
                if neighbor in explored:
                    if cost < states[neighbor][1]:
                        states[neighbor] = (node, cost)
                else:
                    states[neighbor] = (node, cost)
                    insert(neighbor, queue, gh)
                    explored.append(neighbor)

    ret = []
    if node == target:
        while states[node][0] != None:
            ret.append(node)
            node = states[node][0]
        ret.append(node) # append the last node
    ret.reverse()
    return ret

def astar_corner(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    def manhatten(x,y):
        #print(x,y)
        return abs(x[0]-y[0]) + abs(x[1]-y[1])
    def find_closet(x, list):
        min = 9999
        index = 0
        for i in range(len(list)):
            d = manhatten(x, list[i])
            if min > d:
                min = d
                index = i
        return list[index]
    def h(x):
        list = x.goals.copy()
        temp = find_closet(x.position, list)
        d = manhatten(x.position, temp)
        list.remove(temp)
        while list:
            old = temp
            temp = find_closet(old, list)
            d += manhatten(old, temp)
            list.remove(temp)
        return d
    def gh(x):
        return h(x) + x.cost
    
    start = Node(maze.start, 0, list(maze.waypoints))
    states = {}
    for position in maze.indices():
        states[position] = []
    states[start.position].append(start)
    queue = [start]
    
    while queue:
        node = queue[0]
        queue.pop(0)
        if node.position in node.goals:
            node.goals.remove(node.position)
            if not node.goals:
                break
        
        neighbors = maze.neighbors(node.position[0], node.position[1])
        cost = node.cost + 1
        for neighbor in neighbors:
            if maze.navigable(neighbor[0], neighbor[1]):
                temp = find(states, neighbor, node.goals)
                if temp:
                    if cost < temp.cost:
                        temp.update(node, cost)
                else:
                    temp = Node(neighbor, cost, node.goals.copy(), node)
                    states[neighbor].append(temp)
                    insert(temp, queue, gh)

    ret = []
    while node != None:
        ret.append(node.position)
        node = node.parent
    ret.reverse()
    return ret


def astar_multiple(maze):
    """
    Runs A star for part 4 of the assignment in the case where there are
    multiple objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []

def fast(maze):
    """
    Runs suboptimal search algorithm for part 5.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []
    
            
