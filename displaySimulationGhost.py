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
        goal = (goalX, goalY)
        currentNode = (self.x,self.y)
        
        children = []
        distance = []
        for child in self.graph.matrix[currentNode]:
            children.append(child)
        
        
        for child in children:
            distance.append(abs(child[0] - goal[0]) + abs(child[1] - goal[1]))
            
        lowest = distance[0]
        for i in distance:
            if i < lowest:
                lowest = i
        return children[distance.index(lowest)]
    
    
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
        else:
            next = self.search(pacmanX,pacmanY)
        
        nextX = next[0]
        nextY = next[1]
        
        if nextX > self.x:
            self.moveRight()
        elif nextX < self.x:
            self.moveLeft()
        elif nextY > self.y:
            self.moveDown()
        elif nextY < self.y:
            self.moveUp()
        else:
            self.changeX = 0
            self.changeY = 0
 
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

    
    