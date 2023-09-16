from simulatedGhost import *
from simulatedPacman import *
from graph import *






class SimulatedGame(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fright = False
        self.frightTimer = 0
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


        self.ghostOne = [9,11]
        self.ghostTwo = [9,11]
        self.ghostThree = [9,11]
        self.ghostFour = [9,11]
        self.goalList = [self.ghostOne, self.ghostTwo, self.ghostFour, self.ghostThree]

        self.score = 0
        
        self.graph = Graph()    
        self.convertToGraph()
        
        
        self.player = SimulatedPlayer(9,11,self.grid, self.graph, self.chromosome)  
        
        self.dotsGroup = [[]]
        self.powerPellets = [[]]
        
        for i, row in enumerate(self.grid):
            self.dotsGroup.append([])
            for j, item in enumerate(row):
                self.dotsGroup[i].append([])
                
                
        self.ghosts = []
        self.ghosts.append(SimulatedGhost(8,9,0,0, self.graph))
        # self.ghosts.append(SimulatedGhost(9,9,0,0, self.graph))
        # self.ghosts.append(SimulatedGhost(10,9,0,0, self.graph))
        # self.ghosts.append(SimulatedGhost(11,9,0,0, self.graph))
        
        
        self.addFood()
        
        
    def runSimulation(self):
        done = False
        # when this loop ends, pacman either died or ate all pellets
        while not done:
            done = self.runLogic()
            
        return (self.score, self.player.stepsTaken)
            
    
        
                        
    def addFood(self):
        # Add the dots inside the game
        # no if x is 7-11 and y is 8-10
        for i, row in enumerate(self.grid):
            for j, item in enumerate(row):

                if item != 0:
                    if((j,i) == (1,1)) or ((j,i) == (17,1)) or ((j,i) == (1,17)) or ((j,i) == (17,17)):
                        self.dotsGroup[i][j] = 2
                        continue
                    if(j,i) == (9,7):
                        self.dotsGroup[i][j] = 3
                    if(i >=8 and i <= 10):
                        if(j>=7 and j <=11):
                            self.dotsGroup[i][j] = 0
                            continue
                    self.dotsGroup[i][j] = 1
                else:
                    self.dotsGroup[i][j] = 0
                    

    def runLogic(self):
        if not self.gameOver:
            self.player.update()
            # print("(" + str(self.player.x) + "," + str(self.player.y) + ")")
            # check if player is on a tile with a pellet
            if self.dotsGroup[self.player.y][self.player.x] == 1:
                self.dotsGroup[self.player.y][self.player.x] = 0
                self.score += 1
            elif self.dotsGroup[self.player.y][self.player.x] == 2:
                self.dotsGroup[self.player.y][self.player.x] = 0
                self.score += 1
                self.fright = True
            elif self.dotsGroup[self.player.y][self.player.x] == 3:
                self.dotsGroup[self.player.y][self.player.x] = 0
                self.score += 2
                
            # check if player collides with ghosts
            if(self.fright):
                self.frightCollisionCheck()
            else:
                if self.checkCollisions():
                    return True
            
            
            
            
            count = 0
            for i in self.ghosts:
                self.getGoals()
                i.update(self.player.newTile, self.goalList[count][0], self.goalList[count][1], self.fright)
                count += 1
            
            #check if player collides with ghosts        
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
            
            if(self.frightTimer >= 40):
                self.frightTimer = 0
                self.fright = False
                
        return self.gameOver
            
                    
                    
    def checkCollisions(self):
        for i in self.ghosts:
            if (self.player.x, self.player.y) == (i.x, i.y):
                return True
            
    def frightCollisionCheck(self):
        for index, ghost in enumerate(self.ghosts):
            if (self.player.x, self.player.y) == (ghost.x, ghost.y):
                self.score += 20
                self.ghosts[index] = SimulatedGhost(8,9,0,0,self.graph)
                
                       


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

