import pygame
from player import Player
from block import Block
from food import Food
from ghost import Ghost
from breadthFirstPlayer import *


SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Game(object):
    def __init__(self):
        self.gameOver = False
        # Create the variable for the score
        self.score = 0
        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None,35)
        # Create the player
        #self.player = Player(288,352,"player.png")
        self.player = Player(9,11,"player.png")
        #loads sound effects
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")

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
                
        # Create the enemies
        self.ghosts = pygame.sprite.Group()
        
        self.ghosts.add(Ghost(256,288,0,-2))
        self.ghosts.add(Ghost(288,288,0,-2))
        self.ghosts.add(Ghost(320,288,0,2))
        self.ghosts.add(Ghost(352,288,0,-2))
        self.addFood()
        
        
                        
    def addFood(self):
        # Add the dots inside the game
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:    
                    self.dotsGroup.add(Food(j*32+12,i*32+12,WHITE,8,8))
                    
                    

    def processEvents(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT or self.gameOver == True: # If user clicked close
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.moveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.moveLeft()
                elif event.key == pygame.K_UP:
                    self.player.moveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.moveDown()
                elif event.key == pygame.K_ESCAPE:
                    self.gameOver = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stopMoveRight()
                elif event.key == pygame.K_LEFT:
                    self.player.stopMoveLeft()
                elif event.key == pygame.K_UP:
                    self.player.stopMoveUp()
                elif event.key == pygame.K_DOWN:
                    self.player.stopMoveDown()

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
            
            
            ghostCollisionList = pygame.sprite.spritecollide(self.player,self.ghosts,True)
            if len(ghostCollisionList) > 0:
                self.player.explosion = True
                
                
            self.gameOver = self.player.game_Over
            
            
            self.ghosts.update()
            
            
            if not self.dotsGroup:
                self.gameOver = True
            

    def displayFrame(self,screen):
        # First, clear the screen to black.
        screen.fill(BLACK)
        #draws game
        self.horizontalBlocks.draw(screen)
        self.verticalBlocks.draw(screen)
        drawEnviroment(screen)
        self.dotsGroup.draw(screen)
        self.ghosts.draw(screen)
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
                                

