import pygame
from player import Player
from block import Block
from food import Food
from breadthFirstPlayer import *
import random
from pathFindPlayer import *
from graph import *



SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class SimulatingAnnealingGame(object):
    def __init__(self):
        
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
        
        self.graph = Graph()
        self.convertToGraph()
        self.path = []
        self.partialPath = []
        self.gameOver = False
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        # Create the player
        #self.player = Player(288,352,"player.png")
        self.player = PathFindPlayer(9,11,"player.png")
        #loads sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        
        
        
        self.grid = enviroment()
        
        self.places = [(1,1), (8,1), (12,5), (17,5),(4,11), (12,13), (1,17), (17,17), (9,15), (14,12)]
        
        
        # Create the blocks that will set the paths where the player can go
        self.horizontalBlocks = pygame.sprite.Group()
        self.verticalBlocks = pygame.sprite.Group()
        self.topLeftBlocks = pygame.sprite.Group()
        self.topRightBlocks = pygame.sprite.Group()
        self.bottomLeftBlocks = pygame.sprite.Group()
        self.bottomRightBlocks = pygame.sprite.Group()
        self.leftBlocks = pygame.sprite.Group()
        self.rightBlocks = pygame.sprite.Group()
        self.topBlocks = pygame.sprite.Group()
        self.bottomBlocks = pygame.sprite.Group()
        
        self.blocksList = [None, self.horizontalBlocks,self.verticalBlocks, None,self.topLeftBlocks,self.topRightBlocks, self.bottomLeftBlocks, self.bottomRightBlocks, self.leftBlocks, self.rightBlocks, self.topBlocks, self.bottomBlocks]
        
        
        # Create a group for the dots on the screen
        self.dotsGroup = pygame.sprite.Group()
        # creates the walls
        #each item # represents a different type of wall
        # see list above drawEnviroment() for meaning of numbers
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                #adds all types of paths to their respective groups
                if item == 1:
                    self.horizontalBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.verticalBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 4:
                    self.topLeftBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 5:
                    self.topRightBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 6:
                    self.bottomLeftBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 7:
                    self.bottomRightBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 8:
                    self.leftBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 9:
                    self.rightBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 10:
                    self.topBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 11:
                    self.bottomBlocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
            
        self.addFood()
        self.genNewPath()
        
        
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
                    
                        
    def addFood(self):
        # Add the dots inside the game
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    if (j,i) in self.places:
                        self.dotsGroup.add(Food(j*32+12,i*32+12,WHITE,8,8))
                    
                    
    
    
    def getOrder(self):
        random.shuffle(self.places)
        return self.places
    
    
    def genNewPath(self):
        self.path = []
        currentCoord = (self.player.x, self.player.y)
        self.getOrder()
        for i in range(10):
            if i != 0:
                currentCoord = self.places[i-1]
            goalCoord = self.places[i]
            self.path.insert(0, self.search(currentCoord, goalCoord))
            
        return self.nodesToPath()
                    

    def search(self,currentCoord, goalCoord):
        goal = goalCoord
        currentNode = currentCoord
        frontier = [currentNode]
        frontierParents = [None]
        explored = {}
        prevNode = None
        while frontier:
            currentNode = frontier.pop(0)
            prevNode = frontierParents.pop(0)
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
                    

    def navigatePath(self):
        direction = None
        if self.player.newTile == True and self.path:
            # if not (self.player.rect.x == self.player.prevX or self.player.rect.y == self.player.prevY):
            direction = self.path.pop(-1)
            
            self.player.stopMoveDown()
            self.player.stopMoveLeft()
            self.player.stopMoveRight()
            self.player.stopMoveUp()
            if direction == "left":
                self.player.moveLeft()
            if direction == "right":
                self.player.moveRight()
            if direction == "up":
                self.player.moveUp()
            if direction == "down":
                self.player.moveDown()
            self.player.prevX = self.player.rect.x/32
            self.player.prevY = self.player.rect.y/32
            
            
    def processEvents(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
        
        
        if  self.gameOver == True:
            return True
        
        if not self.path:
            self.genNewPath()
            self.path = self.nodesToPath()
            
        
        self.navigatePath()

        return False

    def runLogic(self):
        if not self.gameOver:
            self.player.update(self.blocksList)
            pelletHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup,True)
            # When the pelletHitList contains one sprite that means that player hit a dot
            if len(pelletHitList) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1

                
            self.gameOver = self.player.game_Over            
            
            if not self.dotsGroup:
                self.gameOver = True
            
            
    def nodesToPath(self):
        backwardsPath = []
        currentSpace = self.places[-1]
        for i in range(len(self.path)):
            # dict = self.path[i]
            
            prevSpace = self.path[i][currentSpace]
            while prevSpace is not None:
                if (prevSpace == (18,9) and currentSpace == (0,9)):
                    backwardsPath.append("right")
                    backwardsPath.append("right")
                elif (prevSpace == (0,9) and currentSpace == (18,9)):
                    backwardsPath.append("left")
                    backwardsPath.append("left")
                elif(prevSpace[0] > currentSpace[0]):
                    backwardsPath.append("left")
                elif(prevSpace[0] < currentSpace[0]):
                    backwardsPath.append("right")
                elif(prevSpace[1] > currentSpace[1]):
                    backwardsPath.append("up")
                elif(prevSpace[1] < currentSpace[1]):
                    backwardsPath.append("down")
                currentSpace = prevSpace
                prevSpace = self.path[i][currentSpace]
            
        return backwardsPath
            

    def displayFrame(self,screen):
        # First, clear the screen to black.
        screen.fill(BLACK)
        #draws game
        self.horizontalBlocks.draw(screen)
        self.verticalBlocks.draw(screen)
        drawEnviroment(screen)
        self.dotsGroup.draw(screen)
        screen.blit(self.player.image,self.player.rect)
        # Render the text for the score
        text = self.font.render("Score: " + str(self.score),True,GREEN)
        # Put the text on the screen
        screen.blit(text,[0,0])
        # update the screen
        pygame.display.flip()
                    
                    
def enviroment():
    
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 4, 1, 1,10, 1, 1, 1, 5, 0, 4, 1, 1, 1,10, 1, 1, 5, 0], 
             [0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0], 
             [0, 8, 1, 1, 3, 1,10, 1,11, 1,11, 1,10, 1, 3, 1, 1, 9, 0],
             [0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
             [0, 6, 1, 1, 9, 0, 6, 1, 5, 0, 4, 1, 7, 0, 8, 1, 1, 7, 0], 
             [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0], 
             [0, 0, 0, 0, 2, 0, 4, 1,11,10,11, 1, 5, 0, 2, 0, 0, 0, 0], 
             [0, 0, 0, 0, 2, 0, 2, 4,10, 3,10, 5, 2, 0, 2, 0, 0, 0, 0], 
             [1, 1, 1, 1, 3, 1, 9, 8, 3, 3, 3, 9, 8, 1, 3, 1, 1, 1, 1], 
             [0, 0, 0, 0, 2, 0, 2, 6,11,11,11, 7, 2, 0, 2, 0, 0, 0, 0], 
             [0, 0, 0, 0, 2, 0, 6, 1,10, 1,10, 1, 7, 0, 2, 0, 0, 0, 0], 
             [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0], 
             [0, 4, 1, 1, 9, 0, 4, 1, 7, 0, 6, 1, 5, 0, 8, 1, 1, 5, 0], 
             [0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0], 
             [0, 8, 1, 1, 3, 1,11, 1,10, 1,10, 1,11, 1, 3, 1, 1, 9, 0], 
             [0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0], 
             [0, 6, 1, 1,11, 1, 1, 1, 7, 0, 6, 1, 1, 1,11, 1, 1, 7, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
             ]
    
    
    
    grid2 = ((0, 0, 0, 0, 0, 0, 0), 
            (0, 4, 1,10, 1, 5, 0),
            (0, 2, 0, 2, 0, 2, 0),
            (0, 8, 1, 3, 1, 9, 0),
            (0, 2, 0, 2, 0, 2, 0),
            (0, 6, 1,11, 1, 7, 0),
            (0, 0, 0, 0, 0, 0, 0)
                )
    
    return grid

def drawEnviroment(screen):

    for i,row in enumerate(enviroment()):
        for j,item in enumerate(row):
            if item == 1:
                #bottom line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                #top line
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            elif item == 2:
                #right line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                #left line
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
            # 4 way intersection
            elif item == 3:
                continue
            #top left corner 
            elif item == 4:
                #top line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                #left line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
            #top right corner
            elif item == 5:
                #top line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
                #right line
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
            #bottom left corner
            elif item == 6:
                #left line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
                #bottom line
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
            #bottom right corner
            elif item == 7:
                #bottom line
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
                #right line
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
            #left only
            elif item == 8:
                #left line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32,i*32+32], 3)
            #right only
            elif item == 9:
                #right line
                pygame.draw.line(screen, BLUE , [j*32+32, i*32], [j*32+32,i*32+32], 3)
            #top only
            elif item == 10:
                #top line
                pygame.draw.line(screen, BLUE , [j*32, i*32], [j*32+32,i*32], 3)
            #bottom only
            elif item == 11:
                #bottom line
                pygame.draw.line(screen, BLUE , [j*32, i*32+32], [j*32+32,i*32+32], 3)
                                

