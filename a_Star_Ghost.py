import ghost
from graph import *
import game as gm

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608


class A_Star_Ghost(ghost.Ghost):
    
    def __init__(self,x,y,change_x,change_y, fileName):
        ghost.Ghost.__init__(self, x,y,change_x,change_y, fileName)
        self.graph = Graph()
        self.convertToGraph()
        self.path = None
        self.newPathNeeded = True
        
        
        
        
    def convertToGraph(self):
        map = gm.enviroment()
        for i,row in enumerate(map):
            for j,item in enumerate(row):
                self.graph.addVertex(j,i)
                currentDirections = self.allowedDirections[item]
                if currentDirections[0]:
                    self.addUp(j,i)
                if currentDirections[1]:
                    self.addDown(j,i)
                if currentDirections[2]:
                    self.addLeft(j,i)
                if currentDirections[3]:
                    self.addRight(j,i)
                    
                    
                    
                    
                    
    def addUp(self,currentX,currentY, weight = 1):
        self.graph.addEdge(currentX,currentY,currentX,currentY-1, weight)
        
    def addDown(self,currentX,currentY, weight = 1):
        self.graph.addEdge(currentX,currentY,currentX,currentY+1, weight)
    
    def addRight(self,currentX,currentY, weight = 1):
        if (currentX+1)*32 >= gm.SCREEN_WIDTH:
            self.graph.addEdge(currentX,currentY,0,currentY, weight)
        else:
            self.graph.addEdge(currentX,currentY,currentX+1,currentY, weight)
        
    def addLeft(self,currentX,currentY, weight = 1):
        if (currentX) == 0:
            self.graph.addEdge(currentX,currentY,(gm.SCREEN_WIDTH//32)-1,currentY, weight)
        else:
            self.graph.addEdge(currentX,currentY,currentX-1,currentY, weight)
            
            
            
            
            
    def update(self, newTile, x, y):
        if self.rect.left < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0
            
        if self.newPathNeeded == False and newTile == True:
            self.newPathNeeded = True
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0 and self.newPathNeeded:
            self.findPath(x,y)
            self.newPathNeeded = False
        if not self.path and (self.rect.x % 32 == 0 and self.rect.y % 32 == 0):
            self.changeX = 0
            self.changeY = 0
        else:
            self.navigatePath()
        

        
        self.rect.x += self.changeX
        self.rect.y += self.changeY
        
        
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0:
            self.x = self.rect.x/32
            self.y = self.rect.y/32
        
        
                    
        
        
        
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
            
        
        self.path = backwardsPath
        return
    
    
    def navigatePath(self):
        print
        direction = None
        if self.rect.x % 32 == 0 and self.rect.y % 32 == 0 and self.path:
            if not (self.rect.x == self.prevX or self.rect.y == self.prevY):
                direction = self.path.pop()
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
                    ucsAndGreedyWeight = nodeWeight + (  abs(frontier[i][0]-goal[0])  +  abs(frontier[i][1]-goal[1])    )
                if i == 0:
                    ucsAndGreedyWeight = nodeWeight + (  abs(frontier[i][0]-goal[0])  +  abs(frontier[i][1]-goal[1])    )
                    lowestPathCost = ucsAndGreedyWeight
                elif lowestPathCost > ucsAndGreedyWeight:
                    indexOfLowestCostPath = i
                    lowestPathCost = ucsAndGreedyWeight
            
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