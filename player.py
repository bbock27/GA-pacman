import pygame

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608

# Define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)

class Player(pygame.sprite.Sprite):
    changeX = 0
    changeY = 0
    explosion = False
    game_Over = False
    moveSpeed = 4

    def __init__(self,x,y,filename):
        self.x = x
        self.y = y
        self.newTile = True
        self.prevX = -1
        self.prevY = -1
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)
        self.blocksList = []
        self.currentDirection = "right"
        # self.moveLeft()
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
        
        
    def checkCollision(self, index, blockSet):
        wallDirections = self.allowedDirections.get((index))
        wallDirections = [not element for element in wallDirections]
        for block in pygame.sprite.spritecollide(self, blockSet, False):
            if  (wallDirections[0]):
                if self.rect.centery < block.rect.centery:
                        self.rect.centery = block.rect.centery
            if  (wallDirections[1]):
                if self.rect.centery > block.rect.centery:
                        self.rect.centery = block.rect.centery
            if  (wallDirections[2]):
                if self.rect.centerx < block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
            if  (wallDirections[3]):
                if self.rect.centerx > block.rect.centerx:
                        self.rect.centerx = block.rect.centerx
            
            
        
    

    def update(self, blocksList):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0
            self.rect.x += self.changeX
            self.rect.y += self.changeY
            self.blocksList = blocksList
            for i, currentBlockType in enumerate(self.blocksList):
                if(currentBlockType is not None):
                    self.checkCollision(i, currentBlockType)
            if self.rect.x % 32 == 0 and self.rect.y % 32 == 0 and not (self.prevX == self.rect.x and self.prevY == self.rect.y):
                self.newTile = True
            else:
                self.newTile = False
            self.prevX = self.rect.x
            self.prevY = self.rect.y
        else:
            self.game_Over = True
            
            
            
            
    def checkGameOver(self):
        if Player.game_Over == True:
            return True
            

    def moveRight(self):
        self.changeX = Player.moveSpeed
        self.changeY = 0
        self.currentDirection = "right"
        # changes orientation of pacman
        self.image = self.playerImage
    def moveLeft(self):
        self.changeX = -Player.moveSpeed
        self.changeY = 0
        self.currentDirection = "left"
        # changes orientation of pacman
        self.image = pygame.transform.flip(self.playerImage,True,False)

    def moveUp(self):
        self.changeY = -Player.moveSpeed
        self.changeX = 0
        self.currentDirection = "up"
        # changes orientation of pacman
        self.image = pygame.transform.rotate(self.playerImage,90)

    def moveDown(self):
        self.changeY = Player.moveSpeed
        self.changeX = 0
        self.currentDirection = "down"
        # changes orientation of pacman
        self.image = pygame.transform.rotate(self.playerImage,270)





    def stopMoveRight(self):
        #if self.changeX != 0:
        self.changeX = 0

    def stopMoveLeft(self):
        #if self.changeX != 0:
            
        self.changeX = 0

    def stopMoveUp(self):
        #if self.changeY != 0:
            
        self.changeY = 0

    def stopMoveDown(self):
        #if self.changeY != 0:
            
        self.changeY = 0

        
