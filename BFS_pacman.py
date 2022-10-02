import pygame
import player
import game as gm
from node import *
from graph import *

class BFS_pacman(player.Player):
    
    def __init__(self, x, y, fileName):
        
        player.Player.__init__(self, x, y, fileName)
        self.graph = Graph()
        #values = (up, down, left, right)
        self.directions = {0:(False,False,False,False),
                           1:(False,False,True,True), 
                           2:(True,True,False,False), 
                           3:(True,True,True,True), 
                           4:(False,True,False,True),
                           5:(False,True,True,False),
                           6:(True,False,False,True),
                           7:(True,False,True,False),
                           8:(True,True,False,True),
                           9:(True,True,True,False),
                           10:(False,True,True,True),
                           11:(True,False,True,True)}
        
        
        self.convertToGraph()
        self.path = []
        self.prevX = -1
        self.prevY = -1
    
    def BFS_Search(self, goalX, goalY):
        goal = (goalX,goalY)
        currentNode = (self.x,self.y)
        frontier = [currentNode]
        frontierParents = [None]
        explored = {}
        prevNode = None
        while frontier:
            currentNode = frontier.pop(0)
            prevNode = frontierParents.pop(0)
            if currentNode == goal:
                explored.update({currentNode:prevNode})
                return explored
            
            if currentNode not in explored.keys():
                explored.update({currentNode:prevNode})
                for child in self.graph.matrix[currentNode]:
                    frontier.append(child)
                    frontierParents.append(currentNode)
            
            
            
            
    def findPath(self, goalX, goalY):
        path = self.BFS_Search(goalX, goalY)
        if path is None:
            return
        backwardsPath = []
        
        currentSpace = (goalX,goalY)
        prevSpace = path[currentSpace]
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
            prevSpace = path[currentSpace]
            
        
        return backwardsPath
    
    
    def navigatePath(self):
        direction = None
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0 and self.path:
            if not (self.rect.x == self.prevX or self.rect.y == self.prevY):
                direction = self.path.pop()
                self.stopMoveDown()
                self.stopMoveLeft()
                self.stopMoveRight()
                self.stopMoveUp()
            if direction == "left":
                self.moveLeft()
            if direction == "right":
                self.moveRight()
            if direction == "up":
                self.moveUp()
            if direction == "down":
                self.moveDown()
            self.prevX = self.rect.x/32
            self.prevY = self.rect.y/32
            
            
    def convertToGraph(self):
        map = gm.enviroment()
        for i,row in enumerate(map):
            for j,item in enumerate(row):
                self.graph.addVertex(j,i)
                currentDirections = self.directions[item]
                if currentDirections[0]:
                    self.addUp(j,i)
                if currentDirections[1]:
                    self.addDown(j,i)
                if currentDirections[2]:
                    self.addLeft(j,i)
                if currentDirections[3]:
                    self.addRight(j,i)

    
    def addUp(self,currentX,currentY):
        self.graph.addEdge(currentX,currentY,currentX,currentY-1)
        
    def addDown(self,currentX,currentY):
        self.graph.addEdge(currentX,currentY,currentX,currentY+1)
    
    def addRight(self,currentX,currentY):
        if (currentX+1)*32 >= gm.SCREEN_WIDTH:
            self.graph.addEdge(currentX,currentY,0,currentY)
        else:
            self.graph.addEdge(currentX,currentY,currentX+1,currentY)
        
    def addLeft(self,currentX,currentY):
        if (currentX) == 0:
            self.graph.addEdge(currentX,currentY,(gm.SCREEN_WIDTH//32)-1,currentY)
        else:
            self.graph.addEdge(currentX,currentY,currentX-1,currentY)
    
    