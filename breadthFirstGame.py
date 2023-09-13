from breadthFirstPlayer import BreadthFirstPlayer
from  playerPathFindGame import *
from greedyPlayer import GreedyPlayer

class BreadthFirstGame(PlayerPathFindGame):
    def __init__(self):
        PlayerPathFindGame.__init__(self)
        self.player = GreedyPlayer(9,11,"player.png")