import pygame
import player
import game as gm
from node import *
from graph import *
import pathFindPlayer
from game import *
import random

class UniformCostPlayer(pathFindPlayer.PathFindPlayer):
    
    def __init__(self, x, y, fileName):
        self.weights = enviroment()
        self.rnd = random.Random()
        self.rnd.seed(1)
        self.createWeights()
        pathFindPlayer.PathFindPlayer.__init__(self, x, y, fileName)
        
    # creaetes random weights for every moveable space
    def createWeights(self):
        
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if(item != 0):
                    weight = self.rnd.randint(1,6)
                    self.weights[i][j] = weight
                


    
    
    def search(self, goalX, goalY):
        goal = (goalX,goalY)
        currentNode = (self.x,self.y, 0)
        frontier = [currentNode]
        frontierParents = [None]
        frontierWeights = [0]
        explored = {}
        prevNode = None
        currentWeight = 0
        while frontier:
            lowestPathCost = frontierWeights[0]
            indexOfLowestCostPath = 0
            # finds the lowest cost next move in the frontier
            for i, nodeWeight in enumerate(frontierWeights):
                if explored is not None and frontierParents[i] is not None:
                    # adds the weight of the  node with the weight of the path to get to the node
                    nodeWeight = nodeWeight + explored[frontierParents[i]][1]
                if i == 0:
                    lowestPathCost = nodeWeight
                elif lowestPathCost > nodeWeight:
                    indexOfLowestCostPath = i
                    lowestPathCost = nodeWeight
            
            currentNode = frontier.pop(indexOfLowestCostPath)
            
            prevNode = frontierParents.pop(indexOfLowestCostPath)
            
            currentWeight = frontierWeights.pop(indexOfLowestCostPath)
            
            if explored:
                # adds the weight of the node with the weight of the path to get to the node
                currentWeight = currentWeight + explored[prevNode][1]
            
            
            if currentNode[0:2] == goal:
                # if the node is the goal, add it to the explored dictinoary with the immediate parent and the weight of the path it took to get to the node
                explored.update({currentNode[0:2]:(prevNode, currentWeight)})
                return explored
            
            if currentNode[0:2] not in explored.keys():
                explored.update({currentNode[0:2]:(prevNode, currentWeight)})
                for child in self.graph.matrix[currentNode[0:2]]:
                    frontier.append(child)
                    frontierParents.append(currentNode[0:2])
                    frontierWeights.append(child[2])
            
            
    # only difference from the parent method is taking into account the weights of the path
    def findPath(self, goalX, goalY):
        path = self.search(goalX, goalY)
        if path is None:
            return
        backwardsPath = []
        
        currentSpace = (goalX,goalY)
        prevSpace = path[currentSpace][0]
        while prevSpace is not None:
            if(prevSpace[0] > currentSpace[0]):
                backwardsPath.append("left")
            elif(prevSpace[0] < currentSpace[0]):
                backwardsPath.append("right")
            elif(prevSpace[1] > currentSpace[1]):
                backwardsPath.append("up")
            elif(prevSpace[1] < currentSpace[1]):
                backwardsPath.append("down")
            currentSpace = prevSpace
            prevSpace = path[currentSpace][0]
            
        
        return backwardsPath
            
            
            
            
    # only difference with parent method is the addition of the weight parameter in the add method calls
    def convertToGraph(self):
        map = gm.enviroment()
        for i,row in enumerate(map):
            for j,item in enumerate(row):
                self.graph.addVertex(j,i)
                currentDirections = self.allowedDirections[item]
                if currentDirections[0]:
                    self.addUp(j,i, self.weights[i][j])
                if currentDirections[1]:
                    self.addDown(j,i, self.weights[i][j])
                if currentDirections[2]:
                    self.addLeft(j,i, self.weights[i][j])
                if currentDirections[3]:
                    self.addRight(j,i, self.weights[i][j])