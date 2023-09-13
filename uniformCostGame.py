import playerPathFindGame 
from uniformCostPlayer import *
from uniformCostPlayer import *
import random
from game import *

class UniformCostGame(playerPathFindGame.PlayerPathFindGame):
    def __init__(self):
        playerPathFindGame.PlayerPathFindGame.__init__(self)
        self.player = UniformCostPlayer(9,11,"player.png")
        self.weights = enviroment()
        self.rnd = random.Random()
        self.rnd.seed(10)
        self.createWeights()
        
        
        
        
    def createWeights(self):
        
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if(item != 0):
                    weight = self.rnd.randint(1,9)
                    self.weights[i][j] = weight