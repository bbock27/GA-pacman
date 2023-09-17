import pygame
import random
# import game as gm

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608






class DisplaySimulationGhost(pygame.sprite.Sprite):
    def __init__(self,x,y,change_x,change_y, graph, fileName = "ghost.png"):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.graph = graph
        self.path = None
        self.newPathNeeded = True
        # Set the direction of the ghost
        self.changeX = change_x
        self.changeY = change_y
        self.image = pygame.image.load(fileName)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.x = x
        self.y = y
        self.prevX = -1
        self.prevY = -1
        self.prevDirection = "-"
        self.intersectionIDs = []
        # self.intersectionPoints = self.getIntersectionPosition()
        self.allowedDirections = {0:(False,False,False,False),
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
        
    def search(self, goalX, goalY):
        # goal = (goalX, goalY)
        # currentNode = (self.x,self.y)
        
        # children = []
        # distance = []
        # for child in self.graph.matrix[currentNode]:
        #     children.append(child)
        
        
        # for child in children:
        #     distance.append(abs(child[0] - goal[0]) + abs(child[1] - goal[1]))
            
        # lowest = distance[0]
        # for i in distance:
        #     if i < lowest:
        #         lowest = i
        # return children[distance.index(lowest)]
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
            
            if currentNode[0:2] == (-1.0, 9.0) or currentNode[0:2] == (19.0, 9.0):
                print("error")
            
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
    
    
    def frightSearch(self, goalX, goalY):
        goal = (goalX, goalY)
        currentNode = (self.x,self.y)
        
        children = []
        distance = []
        for child in self.graph.matrix[currentNode]:
            children.append(child)
        
        
        for child in children:
            distance.append(abs(child[0] - goal[0]) + abs(child[1] - goal[1]))
            
        highest = distance[0]
        for i in distance:
            if i > highest:
                highest = i
        return children[distance.index(highest)]
    
    
    def update(self, newTile, pacmanX, pacmanY, fright):
        
        if(fright):
            next = self.frightSearch(pacmanX,pacmanY)
            if(next[0] > self.x):
                next = "right"
            elif(next[0] < self.x):
                next = "left"
            elif(next[1] > self.y):
                next = "down"
            elif(next[1] < self.y):
                next = "up"
        else:
            next = self.search(pacmanX,pacmanY)
            if next is None:
                next = "none"
            else:
                backwardsPath = []
        
                currentSpace = (pacmanX,pacmanY)
                prevSpace = next[currentSpace][0]
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
                    prevSpace = next[currentSpace][0]
                    
                if(len(backwardsPath) == 0):
                    next = "none"
                else:
                    next = backwardsPath.pop()
            
        
        # nextX = next[0]
        # nextY = next[1]
        
        
        if next == "left":
            self.moveLeft()
        elif next == "right":
            self.moveRight()
        elif next == "up":
            self.moveUp()
        elif next == "down":
            self.moveDown()
        else:
            self.changeX = 0
            self.changeY = 0
        # nextX = next[0]
        # nextY = next[1]
        
        # if nextX > self.x:
        #     self.moveRight()
        # elif nextX < self.x:
        #     self.moveLeft()
        # elif nextY > self.y:
        #     self.moveDown()
        # elif nextY < self.y:
        #     self.moveUp()
        # else:
        #     self.changeX = 0
        #     self.changeY = 0
 
        self.x += self.changeX
        self.y += self.changeY
        
        
        
        if(self.y == 9):
            if self.x == 19:
                self.x = 0
            elif self.x == -1:
                self.x = 18
        
        
        self.rect.x = self.x*32
        self.rect.y = self.y*32
 

    
    def moveLeft(self):
        self.changeX = -1
        self.changeY = 0
        
    def moveRight(self):
        self.changeX = 1
        self.changeY = 0
        
    def moveUp(self):
        self.changeX = 0
        self.changeY = -1
        
    def moveDown(self):
        self.changeX = 0
        self.changeY = 1

    
    