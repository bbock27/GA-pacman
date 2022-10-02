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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.playerImage = pygame.image.load(filename).convert()
        self.playerImage.set_colorkey(BLACK)
        self.lives = 5

    def update(self,horizontalBlocks,verticalBlocks,topLeftBlocks,topRightBlocks, bottomLeftBlocks, bottomRightBlocks, leftBlocks, rightBlocks, topBlocks, bottomBlocks):
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

            # These loops will stop pacman from colliding with walls and going through them
            # checks for deviation from center of "hallway" and moves them to the center
            
            
            for block in pygame.sprite.spritecollide(self,horizontalBlocks,False):
                # puts pacmam back into the center of the "hallway" and stops vertical movement
                self.rect.centery = block.rect.centery
                
                
                
            for block in pygame.sprite.spritecollide(self,verticalBlocks,False):
                # puts pacmam back into the center of the "hallway" and stops horizontal movement
                self.rect.centerx = block.rect.centerx
                
                
                
            for block in pygame.sprite.spritecollide(self,topLeftBlocks,False):
                #if pacman is left of the center(colliding with the left wall), move him to the x-center
                if self.rect.centerx < block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                #if pacman is above the center(colliding with top wall), move him to the y-center
                if self.rect.centery < block.rect.centery:
                    self.rect.centery = block.rect.centery
                
                
                
            for block in pygame.sprite.spritecollide(self,topRightBlocks,False):
                #if pacman is right of the center(colliding with the right wall), move him to the center
                if self.rect.centerx > block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                #if pacman is above the center(colliding with top wall), move him to the y-center
                if self.rect.centery < block.rect.centery:
                    self.rect.centery = block.rect.centery
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,bottomLeftBlocks,False):
                #if pacman is left of the center(colliding with the left wall), move him to the center
                if self.rect.centerx < block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                #if pacman is below the center(colliding with bottom wall), move him to the y-center
                if self.rect.centery > block.rect.centery:
                    self.rect.centery = block.rect.centery
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,bottomRightBlocks,False):
                #if pacman is right of the center(colliding with the right wall), move him to the center
                if self.rect.centerx > block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                #if pacman is below the center(colliding with bottom wall), move him to the y-center
                if self.rect.centery > block.rect.centery:
                    self.rect.centery = block.rect.centery
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,leftBlocks,False):
                #if pacman is left of the center(colliding with the left wall), move him to the center
                if self.rect.centerx < block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,rightBlocks,False):
                #if pacman is right of the center(colliding with the right wall), move him to the center
                if self.rect.centerx > block.rect.centerx:
                    self.rect.centerx = block.rect.centerx
                    
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,topBlocks,False):
                #if pacman is above the center(colliding with top wall), move him to the y-center
                if self.rect.centery < block.rect.centery:
                    self.rect.centery = block.rect.centery
                    
                    
                    
            for block in pygame.sprite.spritecollide(self,bottomBlocks,False):
                #if pacman is below the center(colliding with bottom wall), move him to the y-center
                if self.rect.centery > block.rect.centery:
                    self.rect.centery = block.rect.centery
        else:
            self.game_Over = True
            
            
            
            
        def checkGameOver(self):
            if Player.game_Over == True:
                return True
            

    def moveRight(self):
        self.changeX = Player.moveSpeed
        # changes orientation of pacman
        self.image = self.playerImage
    def moveLeft(self):
        self.changeX = -Player.moveSpeed
        # changes orientation of pacman
        self.image = pygame.transform.flip(self.playerImage,True,False)

    def moveUp(self):
        self.changeY = -Player.moveSpeed
        # changes orientation of pacman
        self.image = pygame.transform.rotate(self.playerImage,90)

    def moveDown(self):
        self.changeY = Player.moveSpeed
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

        
