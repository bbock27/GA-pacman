import pygame
import game
from player import Player
from block import Block
from food import Food
from ghosts import Ghost
from BFS_pacman import *
from game import *

class BFS_Game(game.Game):
    
    def __init__(self):
        self.goal = (16,1)
        game.Game.__init__(self)
        
        self.player = BFS_pacman(9,11,"player.png")
        
        
        
        
        
        
        
    def addFood(self):
        # Add the dots inside the game
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    if (j,i) == self.goal:
                        self.dotsGroup.add(Food(j*32+12,i*32+12,RED,8,8))
                    else:
                        self.dotsGroup.add(Food(j*32+12,i*32+12,WHITE,8,8))
         
         
         
    def processEvents(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return True
        
        
        if  self.gameOver == True:
            return True
        
        if not self.player.path:
            self.player.path = self.player.findPath(self.goal[0], self.goal[1])
        
        self.player.navigatePath()

        return False
    
    
    
    
    def runLogic(self):
        if not self.gameOver:
            self.player.update(self.horizontalBlocks,self.verticalBlocks,self.topLeftBlocks,self.topRightBlocks, self.bottomLeftBlocks, self.bottomRightBlocks, self.leftBlocks, self.rightBlocks, self.topBlocks, self.bottomBlocks)
            blockHitList = pygame.sprite.spritecollide(self.player,self.dotsGroup,True)
            # When the blockHitList contains one sprite that means that player hit a dot
            if len(blockHitList) > 0:
                # Here will be the sound effect
                self.pacman_sound.play()
                self.score += 1
            blockHitList = pygame.sprite.spritecollide(self.player,self.enemies,True)
            if len(blockHitList) > 0:
                self.player.explosion = True
            self.gameOver = self.player.game_Over
            self.enemies.update()
            if not self.dotsGroup or (self.player.rect.x/32, self.player.rect.y/32) == self.goal:
                self.gameOver = True
    
    
    