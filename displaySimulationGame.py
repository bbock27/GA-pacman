# from breadthFirstPlayer import *
from simulatedGhost import *
from displaySimulationPlayer import *
from graph import *
from block import Block
from food import Food
from displaySimulationGhost import *


BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)


class DisplaySimulatedGame(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
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
        self.gameOver = False
        self.fright = False
        self.frightTimer = 0

        # Create the blocks that will set the paths where the player can go
        self.horizontalBlocks = pygame.sprite.Group()
        self.verticalBlocks = pygame.sprite.Group()
                
        
        # Create a group for the dots on the screen
        self.powerPellets = pygame.sprite.Group()
        self.fruit = pygame.sprite.Group()
        
                    
                    
                    
                    
                    
        self.ghostOne = [9,11]
        self.ghostTwo = [9,11]
        self.ghostThree = [9,11]
        self.ghostFour = [9,11]
        self.goalList = [self.ghostOne, self.ghostTwo, self.ghostFour, self.ghostThree]

        self.score = 0
        
        self.graph = Graph()    
        self.convertToGraph()
        
        
        self.player = DisplaySimulationPlayer(9,11,self.grid, self.graph, self.chromosome, "player.png")  
        
        self.dotsGroup = [[]]
        self.dotsGroup2 = pygame.sprite.Group()

        for i, row in enumerate(self.grid):
            self.dotsGroup.append([])
            for j, item in enumerate(row):
                self.dotsGroup[i].append([])
                
                
        self.ghosts = []
        self.ghosts = pygame.sprite.Group()
        self.ghosts.add(DisplaySimulationGhost(8,9,0,0, self.graph))
        self.ghosts.add(DisplaySimulationGhost(9,9,0,0, self.graph))
        self.ghosts.add(DisplaySimulationGhost(10,9,0,0, self.graph))
        self.ghosts.add(DisplaySimulationGhost(11,9,0,0, self.graph))
        
        
        self.addFood()
        
        
    
        
                        
    def addFood(self):
        # Add the dots inside the game
        # no if x is 7-11 and y is 8-10 (inside ghost box)
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):
                if item != 0:
                    # adds power pellets
                    if((j,i) == (1,1)) or ((j,i) == (17,1)) or ((j,i) == (1,17)) or ((j,i) == (17,17)):
                        self.powerPellets.add(Food(j*32+12,i*32+12,RED,8,8))
                        continue
                    #adds fruit
                    if(j,i) == (9,7):
                        self.fruit.add(Food(j*32+12,i*32+12,GREEN,8,8))
                    #gets rid of pellets in the ghost box
                    if(i >=8 and i <= 10):
                        if(j>=7 and j <=11):
                            self.dotsGroup[i][j] = False
                            continue
                    self.dotsGroup[i][j] = True
                    self.dotsGroup2.add(Food(j*32+12,i*32+12,WHITE,8,8))
                else:
                    self.dotsGroup[i][j] = False
                    

    def runLogic(self):
        if not self.gameOver:
            self.player.update()

            pelletHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup2,True)
            if len(pelletHitList) > 0:
                self.score += 1
                
            pelletHitList = pygame.sprite.spritecollide(self.player,self.fruit,True)
            if len(pelletHitList) > 0:
                self.score += 2
                
            pelletHitList = pygame.sprite.spritecollide(self.player,self.powerPellets,True)
            if len(pelletHitList) > 0:
                self.fright = True
                self.score += 1
                
                
            # check if player collides with ghosts
            if(self.fright):
                self.frightCollisionCheck()
            else:
                if self.checkCollisions():
                    return True
            
            
            count = 0
            self.getGoals()
            for ghost in self.ghosts:
                ghost.update(self.player.newTile, self.goalList[count][0], self.goalList[count][1], self.fright)
                count += 1
            
                    

            # check if player collides with ghosts
            if(self.fright):
                self.frightCollisionCheck()
            else:
                if self.checkCollisions():
                    return True
                
                
            self.gameOver = self.player.gameOver
            
            
            if not self.dotsGroup:
                return True
                
            if(self.fright):
                self.frightTimer += 1
                print(self.frightTimer)
            
            if(self.frightTimer >= 10):
                self.frightTimer = 0
                self.fright = False
                
                
        return self.gameOver
            
    def displayFrame(self,screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        # First, clear the screen to black.
        screen.fill(BLACK)
        #draws game
        self.horizontalBlocks.draw(screen)
        self.verticalBlocks.draw(screen)
        self.drawEnviroment(screen)
        self.dotsGroup2.draw(screen)
        self.powerPellets.draw(screen)
        self.ghosts.draw(screen)
        self.fruit.draw(screen)
        screen.blit(self.player.image,self.player.rect)

        pygame.display.flip()        
         
                    
    def checkCollisions(self):
        for i in self.ghosts:
            if (self.player.x, self.player.y) == (i.x, i.y):
                return True
                    
    def frightCollisionCheck(self):
        deadGhosts = []
        for index, ghost in enumerate(self.ghosts):
            if (self.player.x, self.player.y) == (ghost.x, ghost.y):
                self.score += 20
                deadGhosts.append(index)
                print("ghost eaten")
        tempGroup = pygame.sprite.Group()
        for index, ghost in enumerate(self.ghosts):
            if index in deadGhosts:
                tempGroup.add(DisplaySimulationGhost(8,9,0,0, self.graph))
            else:
                tempGroup.add(ghost)
                
        self.ghosts=tempGroup
            
        

    def convertToGraph(self):
        
        for i,row in enumerate(self.grid):
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
        if (currentX+1) >= 19:
            self.graph.addEdge(currentX,currentY,0,currentY, weight)
        else:
            self.graph.addEdge(currentX,currentY,currentX+1,currentY, weight)
        
    def addLeft(self,currentX,currentY, weight = 1):
        if (currentX) == 0:
            self.graph.addEdge(currentX,currentY,18,currentY, weight)
        else:
            self.graph.addEdge(currentX,currentY,currentX-1,currentY, weight)
            
            
            
    def getGoals(self):
        if not self.player.newTile:
            return
        currentX = self.player.x
        currentY = self.player.y

        self.ghostFour = (currentX, currentY)
        
        # forward 4 greedy
        if self.player.currentDirection == "right":
            toSearch = self.grid[currentY]
            for i in range(4):
                if currentX+(i+1) >= len(toSearch):
                    self.ghostTwo = (0,currentY)
                else:
                    self.ghostTwo = (currentX + i+1, currentY)
                    if toSearch[currentX + i+1] == 0:
                        self.ghostTwo = (currentX + i, currentY)
                        break
        elif self.player.currentDirection == "left":
            toSearch = self.grid[currentY]
            for i in range(4):
                if currentX-(i+1) < 0:
                    self.ghostTwo = (len(toSearch)-1, currentY)
                else:
                    self.ghostTwo = (currentX - (i+1), currentY)
                    if toSearch[currentX - (i+1)] == 0:
                        self.ghostTwo = (currentX - i, currentY)
                        break
        elif self.player.currentDirection == "up":
            for i in range(4):
                self.ghostTwo = (currentX, currentY - (i+1))
                if self.grid[currentY-i][currentX] == 0:
                    self.ghostTwo = (currentX, currentY - i)
                    break
        elif self.player.currentDirection == "down":
            for i in range(4):
                self.ghostTwo = (currentX, currentY + (i+1))
                if self.grid[currentY-i][currentX] == 0:
                    self.ghostTwo = (currentX, currentY + i)
                    break
                
                
                
        # back 4 greedy
        if self.player.currentDirection == "left":
            toSearch = self.grid[currentY]
            for i in range(4):
                if currentX+(i+1) >= len(toSearch):
                    self.ghostTwo = (0,currentY)
                else:
                    self.ghostThree = (currentX + i+1, currentY)
                    if toSearch[currentX + i+1] == 0:
                        self.ghostThree = (currentX + i, currentY)
                        break
        elif self.player.currentDirection == "right":
            toSearch = self.grid[currentY]
            for i in range(4):
                if currentX-(i+1) < 0:
                    self.ghostTwo = (len(toSearch)-1, currentY)
                else:
                    self.ghostThree = (currentX - (i+1), currentY)
                    if toSearch[currentX - (i+1)] == 0:
                        self.ghostThree = (currentX - i, currentY)
                        break
        elif self.player.currentDirection == "down":
            for i in range(4):
                self.ghostThree = (currentX, currentY - (i+1))
                if self.grid[currentY-i][currentX] == 0:
                    self.ghostThree = (currentX, currentY - i)
                    break
        elif self.player.currentDirection == "up":
            for i in range(4):
                self.ghostThree = (currentX, currentY + (i+1))
                if self.grid[currentY-i][currentX] == 0:
                    self.ghostThree = (currentX, currentY + i)
                    break
                    
                    
        # UCS goal
        if self.player.currentDirection == "left":
            if currentX <= 1:
                print
                # self.UCS_Goal = (1,1)
            else:
                if not self.grid[currentY][currentX-1] == 0:
                    self.ghostOne = (currentX-1, currentY)
                    if not self.grid[currentY][currentX-2] == 0:
                        self.ghostOne = (currentX-2, currentY)
                        if not self.grid[currentY+1][currentX-2] == 0:
                            self.ghostOne = (currentX-2, currentY+1)
                            if not self.grid[currentY+2][currentX-2] == 0:
                                self.ghostOne = (currentX-2, currentY+2)
                
        elif self.player.currentDirection == "right":
            if currentX >= len(self.grid[0])-2:
                print
                # self.UCS_Goal = (1,1)
            else:
                if not self.grid[currentY][currentX+1] == 0:
                    self.ghostOne = (currentX+1, currentY)
                    if not self.grid[currentY][currentX+2] == 0:
                        self.ghostOne = (currentX+2, currentY)
                        if not self.grid[currentY+1][currentX+2] == 0:
                            self.ghostOne = (currentX+2, currentY+1)
                            if not self.grid[currentY+2][currentX+2] == 0:
                                self.ghostOne = (currentX+2, currentY+2)
                            
                            
        elif self.player.currentDirection == "down":
            if not self.grid[currentY+1][currentX] == 0:
                self.ghostOne = (currentX, currentY+1)
                if not self.grid[currentY+2][currentX] == 0:
                    self.ghostOne = (currentX, currentY+2)
                    if not self.grid[currentY+2][currentX-1] == 0:
                        self.ghostOne = (currentX-1, currentY+2)
                        if not self.grid[currentY+2][currentX-2] == 0:
                            self.ghostOne = (currentX-2, currentY+2)
                            
        elif self.player.currentDirection == "up":
            if not self.grid[currentY-1][currentX] == 0:
                self.ghostOne = (currentX, currentY-1)
                if not self.grid[currentY-2][currentX] == 0:
                    self.ghostOne = (currentX, currentY-2)
                    if not self.grid[currentY-2][currentX-1] == 0:
                        self.ghostOne = (currentX-1, currentY-2)
                        if not self.grid[currentY-2][currentX-2] == 0:
                            self.ghostOne = (currentX-2, currentY-2)
        
        
        self.goalList = [self.ghostOne, self.ghostTwo, self.ghostFour, self.ghostThree]




    def drawEnviroment(self, screen):
        #1 - horizontal
        #2 - vertical
        #3 - 4 way
        #4 - top left
        #5 - top right
        #6 - bottom left
        #7 - bottom right
        #8 - left only
        #9 - right only
        #10 - top only
        #11 - bottom only
        for i,row in enumerate(self.grid):
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
                                

