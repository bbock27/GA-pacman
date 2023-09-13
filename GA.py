from simulatedGame import *
from random import randint




class GA():
    def __init__(self):
        self.currPopulation = []
        self.currPopFitness = []
        self.genSize = 3000
        self.genCount = 1000
        self.chromosomeSize = 1500
        # total num of dots is 166
        for i in range(self.genSize):
            self.currPopFitness.append([0,""])
            
        self.scoreList = []
        
        
    def runGA(self):
        self.genInitialPop()
        
        # runs a generation each iteration
        for generation in range(self.genCount):
            print(generation)
            self.scoreList = []
            
            #evaluates an individual each iteration
            for i in range(self.genSize):
                self.currPopFitness[i] = [self.evalFitness(self.currPopulation[i]), self.currPopulation[i]]
            # sorts the list by each entry's first element(score)
            self.currPopFitness.sort(reverse = True, key = lambda x:x[0])
                
            #all the print statements are for obtaining the data afterwords.
            print(str(self.currPopFitness[0][0]) + "--" + self.currPopFitness[0][1])
            print(str(self.currPopFitness[1][0]) + "--" + self.currPopFitness[1][1])
            print(str(self.currPopFitness[2][0]) + "--" + self.currPopFitness[2][1])
            print(str(self.currPopFitness[3][0]) + "--" + self.currPopFitness[3][1])
            self.crossover()
            print("")
            print(self.currPopulation[0])
            
            
        print("currPopfitness")
        print(self.currPopFitness) 
        print("raw scores")
        self.scoreList.sort(reverse = True)
        print(self.scoreList)
        
        return self.currPopFitness
                
                
        

    
    
    def crossover(self):
        
        self.currPopulation[0] = self.currPopFitness[0][1]
        self.currPopulation[1] = self.currPopFitness[1][1]
        for i in range(2, self.genSize, 2):
            chromo1 = self.currPopFitness[i][1]
            chromo2 = self.currPopFitness[i+1][1]
            crossoverPoint = randint((len(chromo1)//2) - 10,(len(chromo1)//2) + 10)
            self.currPopulation[i] = chromo1[0:crossoverPoint] + chromo2[crossoverPoint:]
            self.currPopulation[i+1] = chromo2[0:crossoverPoint] + chromo1[crossoverPoint:]
            
            
    
            
            
            
    def genInitialPop(self):
        for i in range(self.genSize):
            chromosome = self.getRandomChromosome()
            self.currPopulation.append(chromosome)
            
            
    def evalFitness(self, chromosome):
        results = SimulatedGame(chromosome).runSimulation()
        self.scoreList.append(results[0])
        # done the weight score vs steps taken. score is prioritized over steps taken
        return ((2*results[0]) - (results[1]//2))
        return results[0]
            
            
            
    def getRandomChromosome(self):
        chromosome = ""
        for i in range(self.chromosomeSize):
            chromosome += str(randint(0,3))        
        return chromosome
        
        
        