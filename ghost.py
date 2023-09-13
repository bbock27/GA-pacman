import pygame
import random
# import game as gm

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608






class Ghost(pygame.sprite.Sprite):
    def __init__(self,x,y,change_x,change_y, fileName = "ghost.png"):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
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
        
        
    # def getNewDirection(self, id):
        
    #     if id == 4:
    #         direction = random.choice(("right","down"))
    #     elif id == 5:
    #         direction = random.choice(("left","down"))
    #     elif id == 6:
    #         direction = random.choice(("right","up"))
    #     elif id == 7:
    #         direction = random.choice(("left","up"))
    #     elif id == 8:
    #         direction = random.choice(("right","up","down"))
    #     elif id == 9:
    #         direction = random.choice(("left","up","down"))
    #     elif id == 10:
    #         direction = random.choice(("left","right","down"))
    #     elif id == 11:
    #         direction = random.choice(("left","right","up"))
    #     else:
    #         direction = random.choice(("left","right","up","down"))
    #     return direction
        
 

    def update(self, *args, **kwargs):
        print("og ghost")

        self.rect.x += self.changeX
        self.rect.y += self.changeY
        
        self.x = self.rect.x
        self.y = self.rect.y
        
        if self.rect.left <= 0:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.left >= SCREEN_WIDTH:
            self.rect.left = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        # if self.rect.topleft in self.intersectionPoints:
        #     index = self.intersectionPoints.index(self.rect.topleft)
        #     direction = self.getNewDirection(self.intersectionIDs[index])

        #     if direction == "left":
        #         self.moveLeft()
        #     elif direction == "right":
        #         self.moveRight()
        #     elif direction == "up":
        #         self.moveUp()
        #     elif direction == "down":
        #         self.moveDown()
        #     self.prevDirection = direction
                
    def moveLeft(self):
        self.changeX = -2
        self.changeY = 0
        
    def moveRight(self):
        self.changeX = 2
        self.changeY = 0
        
    def moveUp(self):
        self.changeX = 0
        self.changeY = -2
        
    def moveDown(self):
        self.changeX = 0
        self.changeY = 2

    # def getIntersectionPosition(self):
    #     items = []
        
    #     for i,row in enumerate(gm.enviroment()):
    #         for j,item in enumerate(row):
    #             if item > 2:
    #                 items.append((j*32,i*32))
    #                 self.intersectionIDs.append(item)

    #     return items
    
    
    