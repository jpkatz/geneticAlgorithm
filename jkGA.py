# -*- coding: utf-8 -*-
import random

#going to do elitism for survivor selection
#would be cool to do based on age -> method that increments age


def main(n):
    #book keeping for the random number    
    
    #specifying some parameters
    populationTotal = 2000
    probMutate = 0.1
    generations = 50
    tournamentAmount = 500
    offspringCount = 300
    
    
    #constructing the population
    initialIndividuals = []
    for i in range(populationTotal):
        initialIndividuals.append(Individual(n,probMutate,0))
    
    population = Population(initialIndividuals,offspringCount)
    
    for i in range(generations):
        population.crossover(tournamentAmount)
        population.survivorSelection()
        individuals = population.individuals            
    
    fitness = []
    for i in range(populationTotal):
        fitness.append(individuals[i].fitness)
    idx = fitness.index(min(fitness))
    return individuals[idx].chromosome

    
class Individual:
    
    def __init__(self,n,probMutate,initial=0):
        self.n = n
        self.probMutate = probMutate
        if initial == 0:
            self.initialize()
        else:
            self.chromosome = initial
        self.getFitness()
        
    def initialize(self):
        self.chromosome = [random.randint(0,1) for _ in range(self.n)]
        
    def mutate(self):
        if random.random()<self.probMutate:
            idx = random.randint(0,self.n-1)
            self.chromosome[idx] = self.chromosome[idx]*(-1)+1
    
    def getFitness(self):
        self.fitness = fitnessFunction(self.chromosome)



class Population():
    
    def __init__(self,individuals,offspringCount):
        self.individuals = individuals
        self.n = len(individuals) #total number of population
        self.offspringCount = offspringCount
        self.chromosomeLength = len(individuals[0].chromosome)
        self.mutationProb = individuals[0].probMutate
        
        
    def crossover(self,k):
        #gets parents that will reproduce
        parents = self.getCandidates(k)
        
        self.children = []
        for i in range(self.offspringCount):
            crossoverPoint = random.randint(0,len(self.individuals[0].chromosome))
            parent1 = parents[2*i]
            parent2 = parents[2*i+1]
            self.children.append(self.individuals[parent1].chromosome[:crossoverPoint]+
                self.individuals[parent2].chromosome[crossoverPoint:])

        
    def getCandidates(self,k):
        parents = []
        for i in range(self.offspringCount):
            for j in range(2):
                potentialParent = random.sample(range(self.n),k)
                idx = 0
                #tournamenet
                for l in range(1,k):
                    fitness1 = self.individuals[potentialParent[idx]].fitness
                    fitness2 = self.individuals[potentialParent[l]].fitness
                    if fitness1 > fitness2:
                        idx = l
                parents.append(potentialParent[idx])
        return parents
        
    def survivorSelection(self):
        #get all fitness values
        fitnessValues = []
        for i in range(self.n):
            fitnessValues.append(self.individuals[i].fitness)
        #get indices of population to remove
        idx = []    
        for i in range(self.offspringCount):
            idx.append(fitnessValues.index(min(fitnessValues)))
            fitnessValues[idx[i]] = 1e6
        #replace the indices with children
        #sort from highest to smallest to delete entries without repercussions
        idx.sort(reverse=True)
        for i in range(self.offspringCount):
            del self.individuals[idx[i]]
            newChild = Individual(self.chromosomeLength,self.mutationProb,self.children[i])
            newChild.mutate()
            self.individuals.append(newChild)
        
def fitnessFunction(chromosome):
    sum=0
    for i in range(len(chromosome)):
        sum += weights[i]*chromosome[i]
    return sum

if __name__ == '__main__':
    n = 100
    #seed = 100
    #random.seed(seed)
    trials = 100
    stats = 0
    for trial in range(trials):
        weights = [random.choice([-1,1]) for _ in range(n)]
        correctSolution = [int((weights[i]-1)/(-2)) for i in range(len(weights))]
        solution = main(n)
        if correctSolution==solution:
            stats+=1
    if trials ==1:
        print('The weights are:           ', weights)
        print('The correct solution is:    ',  correctSolution )
        print('Genetic Algorithm Solution: ',solution)
    print('Percent correct solutions:',stats/trials*100)
    