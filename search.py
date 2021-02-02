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
    def __init__(self, position=(0,0), cost=0, pastNode=None):
        self.position = position
        self.pastNode = pastNode
        self.cost = cost
    def update(self, pastNode, cost):
        self.pastNode = pastNode
        self.cost = cost
    def __repr__(self):
        return str(self.position)

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
                queue.append(Node(neighbor, 0, node))
                explored.append(neighbor)

    ret = []
    if node.position == target:
        while node != None:
            ret.append(node.position)
            node = node.pastNode
    ret.reverse()
    return ret


def astar_single(maze):
    """
    Runs A star for part 2 of the assignment.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
    """
    return []

def astar_corner(maze):
    """
    Runs A star for part 3 of the assignment in the case where there are four corner objectives.

    @param maze: The maze to execute the search on.

    @return path: a list of tuples containing the coordinates of each state in the computed path
        """
    return []

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
    
            
