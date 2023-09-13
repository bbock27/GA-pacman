import pygame
import player
import game as gm
from node import *
from graph import *
import pathFindPlayer

class GreedyPlayer(pathFindPlayer.PathFindPlayer):
    
    
    def __init__(self, x, y, fileName):
        
        pathFindPlayer.PathFindPlayer.__init__(self, x, y, fileName)
        print ("greedy")
        #values = (up, down, left, right)
        # self.directions = {0:(False,False,False,False),
        #                    1:(False,False,True,True), 
        #                    2:(True,True,False,False), 
        #                    3:(True,True,True,True), 
        #                    4:(False,True,False,True),
        #                    5:(False,True,True,False),
        #                    6:(True,False,False,True),
        #                    7:(True,False,True,False),
        #                    8:(True,True,False,True),
        #                    9:(True,True,True,False),
        #                    10:(False,True,True,True),
        #                    11:(True,False,True,True)}
    
    
    def search(self, goalX, goalY):
        goal = (goalX, goalY)
        currentNode = (self.x,self.y)
        frontier = [currentNode]
        frontierParents = [None]
        frontierDistances = [0]
        explored = {}
        prevNode = None
        
        while frontier:
            
            for i, nodeDistance in enumerate(frontierDistances):
                indexOfLowestCostPath = 0
                if i == 0:
                    lowestPathCost = nodeDistance
                elif lowestPathCost > nodeDistance:
                    indexOfLowestCostPath = i
                    lowestPathCost = nodeDistance
            currentNode = frontier.pop(indexOfLowestCostPath)
            prevNode = frontierParents.pop(indexOfLowestCostPath)
            
            if currentNode[0:2] == goal:
                explored.update({currentNode[0:2]:prevNode[0:2]})
                return explored
            
            if currentNode[0:2] not in explored.keys():
                if prevNode is not None:
                    explored.update({currentNode[0:2]:prevNode[0:2]})
                else:
                    explored.update({currentNode[0:2]:prevNode})
                for child in self.graph.matrix[currentNode[0:2]]:
                    frontier.append(child[0:2])
                    frontierParents.append(currentNode[0:2])
                    frontierDistances.append(abs(goalX-currentNode[0]) + abs(goalY-currentNode[1]))
                    
                    
                    
                    
                    
        
        # currentDistance = abs(goalX-self.x) + abs(goalY-self.y)
        # explored = {currentNode:None}
        # while currentDistance > 0:
        #     if(currentNode[0:2] == goal):
        #         return explored
        #     lowest = None
        #     lowestDistance = None
        #     currentDistance = abs(goalX-currentNode[0]) + abs(goalY-currentNode[1])
        #     for child in self.graph.matrix[currentNode[0:2]]:
        #         if lowest is None:
        #             lowestDistance = abs(goalX-child[0]) + abs(goalY-child[1])
        #             lowest = child[0:2]
        #         else:
        #             if lowestDistance > (abs(goalX-child[0]) + abs(goalY-child[1])):
        #                 lowestDistance = abs(goalX-child[0]) + abs(goalY-child[1])
        #                 lowest = child[0:2]
                
        #     explored.update({lowest[0:2]:currentNode[0:2]})
        #     currentNode = lowest[0:2]
            
            
            