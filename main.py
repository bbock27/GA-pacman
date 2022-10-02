import pygame
from game import Game
from BFS_pacman import *
from BFS_game import *

SCREEN_WIDTH = 608
SCREEN_HEIGHT = 608

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    game = Game()
    # game = BFS_Game()
    
    

    while not done:
        # Process events
        done = game.processEvents()
        # Game logic here
        game.runLogic()
        # Draw the current frame
        game.displayFrame(screen)
        # Limit to 30 fps
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    main()