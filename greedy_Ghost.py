import ghost
from graph import *
import game as gm

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608


class Greedy_Ghost(ghost.Ghost):
    
    def __init__(self,x,y,change_x,change_y, fileName):
        ghost.Ghost.__init__(self, x,y,change_x,change_y, fileName)
        self.graph = Graph()
        self.convertToGraph()
        self.path = None
        self.newPathNeeded = True
        
        
        
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
            if currentNode[0:2] == (19.0, 9.0) or currentNode[0:2] == (-1.0, 9.0):
                print("error")
            if currentNode[0:2] == goal:
                if prevNode is None:
                    explored.update({currentNode[0:2]:None})
                else:
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
            
        
        self.path = backwardsPath
        return
    
    
    def navigatePath(self):
        direction = None
        if(self.path is None):
            self.changeX = 0
            self.changeY = 0
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
            
            
            
            
        