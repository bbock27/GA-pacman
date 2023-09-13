from simulatedAnnealingGame import *
import random
import math


class SimulatedAnnealing(object):
    
    def __init__(self):
        self.path = 0
        self.game = SimulatingAnnealingGame()
        self.temp = 0
        
        
        
    def findNeighbor(self):
        return  self.game.genNewPath()
        
    def objective(self, path):
        return len(path)
        

    
    def coolTemp(self):
        self.temp -= .01
    
    # simulated annealing algorithm
    def simulated_annealing(self, startTemp):
        self.temp = startTemp
        betterCandidates = []
        betterCandidatesEval = [] 
        worseCandidates = []
        worseCandidatesEval = []
        # generate an initial point
        initialPath = self.game.genNewPath()
        # evaluate the initial point
        initialEval = self.objective(initialPath)
        # current working solution
        bestEval = initialEval
        # run the algorithm
        while self.temp >= 0.5:
            print (self.temp)
            for i in range(3):
                # take a step
                candidate = self.findNeighbor()
                # evaluate candidate point
                candidateEval = self.objective(candidate)
                # check for new best solution
                if candidateEval < bestEval:
                    # store new best point
                    betterCandidates.append(candidate)
                    betterCandidatesEval.append(candidateEval)
                else:
                    worseCandidates.append(candidate)
                    worseCandidatesEval.append(candidateEval)
            if len(betterCandidates) != 0:
                randomIndex = random.randint(0, len(betterCandidates)-1)
                curr, bestEval = betterCandidates[randomIndex], betterCandidatesEval[randomIndex]
                self.coolTemp()
                continue
                
            randomIndex = random.randint(0, len(worseCandidates)-1)
            diff = bestEval - worseCandidatesEval[randomIndex] 
            # calculate temperature for current epoch
            probablility = 1/math.exp(diff/self.temp)
            self.coolTemp()
            # check if we should keep the new point
            if probablility > .01:
                curr, bestEval = worseCandidates[randomIndex], worseCandidatesEval[randomIndex]
                # store the new current point
        return [curr, bestEval]