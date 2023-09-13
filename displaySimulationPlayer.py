from node import *
from graph import *
import player
import pygame


# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)


class DisplaySimulationPlayer(pygame.sprite.Sprite):
    
    def __init__(self, x, y, map, graph, chromosome, filename):
        
        
        self.graph = graph
        self.stepsTaken = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)
        self.changeX = 0
        self.changeY = 0
        self.gameOver = False
        self.path = chromosome
        self.x = x
        self.y = y
        self.newTile = True
        self.map = map
        #values = (up, down, left, right)
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
        
    
    

    def update(self):
        if not self.gameOver:
            
            self.navigatePath()
            
            self.x += self.changeX
            self.y += self.changeY
            if(self.y == 9):
                if self.x == 19:
                    self.x = 0
                elif self.x == -1:
                    self.x = 18
            self.rect.x = self.x * 32
            self.rect.y = self.y * 32
            
        else:
            self.gameOver = True
    
    
    def navigatePath(self):
        direction = None
        currentDirections = self.allowedDirections[self.map[self.y][self.x]]
        if not self.stepsTaken == len(self.path):
            direction = self.path[self.stepsTaken]
            self.newTile = False
            if direction == "0" and currentDirections[0]:
                self.moveUp()
                self.newTile = True
            elif direction == "1" and currentDirections[1]:
                self.moveDown()
                self.newTile = True
            elif direction == "2" and currentDirections[2]:
                self.moveLeft()
                self.newTile = True
            elif direction == "3" and currentDirections[3]:
                self.moveRight()
                self.newTile = True
            else:
                self.changeX = 0
                self.changeY = 0
            self.stepsTaken += 1
        else:
            self.gameOver = True
            self.changeX = 0
            self.changeY = 0

            
            
    
    
    def moveRight(self):
        self.changeX = 1
        self.changeY = 0
        self.currentDirection = "right"

    def moveLeft(self):
        self.changeX = -1
        self.changeY = 0
        self.currentDirection = "left"


    def moveUp(self):
        self.changeY = -1
        self.changeX = 0
        self.currentDirection = "up"


    def moveDown(self):
        self.changeY = 1
        self.changeX = 0
        self.currentDirection = "down"
