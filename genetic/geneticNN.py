#from . import genotype, neurallayer, neuralnetwork
from .neurallayer import NeuralLayer, ActivationFunctionType
from .genotype import Genotype
from .neuralnetwork import NeuralNetwork
import random, sys, math

# The class represents population of NeuralNetworks and supports genetic algoritms to train NN
class GeneticNN:
    def __init__(self,topology,populationCount,activationFunctionType = ActivationFunctionType.SoftSignFunction, initGenotype = None):
        self.randomizer = random
        self.PopulationCount = populationCount
        self.Topology = topology
        self.ActivationFunctionType = activationFunctionType
        self.NNs = [0 for i in range(populationCount)]
        self.Evaluations = [0.0 for i in range(populationCount)]
            
        # Default min value of inital population parameters   
        self.InitParamMin = -1.0
        self.InitParamMax = 1.0
        # Default probability of a parameter being swapped during crossover
        self.CrossSwapProb = 0.6
        # Default probability of a parameter being mutated
        self.MutationProb = 0.3
        # Default amount by which parameters may be mutated.
        self.MutationAmount = 2.0
        # Default percent of genotypes in a new population that are mutated.
        self.MutationPerc = 1.0
        self.MN = -1000.0
        self.MX = 1000.0
        
         # create NN, init by random values
        for i in range(populationCount):
            self.NNs[i] = NeuralNetwork(activationFunctionType, topology)
            if (initGenotype != None):
                self.NNs[i].SetWeights(initGenotype) # init by default weights (if presented)
            else:
                self.NNs[i].SetRandomWeights(self.InitParamMin, self.InitParamMax) # init by random weights
                
        #build next generation based on default weights
        if (initGenotype != None):
            for i in range(populationCount):
                self.Evaluations[i] = 1
            self.BuildNextGeneration()

# Calculates the fitness of each genotype by the formula: fitness = evaluation / averageEvaluation.
    def DefaultFitnessCalculation(self, currentPopulation):
        # First calculate average evaluation of whole population
        populationSize = 0
        overallEvaluation = 0.0
        for genotype in currentPopulation:
            overallEvaluation += genotype.Evaluation
            populationSize+=1

        averageEvaluation = overallEvaluation / populationSize
        # Now assign fitness with formula fitness = evaluation / averageEvaluation
        for i in range(len(currentPopulation)-1):
            if (abs(averageEvaluation) > sys.float_info.epsilon):
                currentPopulation[i].Fitness = int(genotype.Evaluation / averageEvaluation)
            else:
                currentPopulation[i].Fitness = 1
        return currentPopulation

# Return NeuarlNetwork by index of population member
    def GetNN(self, index):
        return self.NNs[index]

# Set evaluation by index of member
    def SetEvaluation(self, index, evaluation):
            self.Evaluations[index] = evaluation

# Build next generation of NN
    def BuildNextGeneration(self):
        self.randomizer.seed()
        # build genotypes
        genotypes = []
        for i in range(self.PopulationCount):
            g_type = Genotype(self.NNs[i].GetWeights())
            g_type.Evaluation = self.Evaluations[i]
            genotypes.append(g_type)
        #calc fitness
        genotypes = self.DefaultFitnessCalculation(genotypes)
        # sort population
        #for i in range(len(genotypes)):
            #genotypes[i].parameters.sort()
        # Apply Selection
        #intermediatePopulation = self.RemainderStochasticSampling(genotypes)
        # Apply Recombination
        newPopulation = self.RandomRecombination(genotypes, self.PopulationCount)
        # Apply Mutation
        #mutPopulation = self.MutateAllButBestTwo(genotypes) # newPopulation - список генетипов
        # set weights to NN
        for i in range(self.PopulationCount-1):
            self.NNs[i].SetWeights(newPopulation[i].parameters)

# Selection operator for the genetic algorithm, using a method called remainder stochastic sampling.
    def RemainderStochasticSampling(self, currentPopulation):
        intermediatePopulation = currentPopulation
        # Put integer portion of genotypes into intermediatePopulation
        # Assumes that currentPopulation is already sorted
        for i in range(len(currentPopulation)):
            if (currentPopulation[i].Fitness < 1):
                break
            for ii in range(currentPopulation[i].Fitness):
                intermediatePopulation[i] = Genotype(currentPopulation[i].GetParameterCopy())
        # Put remainder portion of genotypes into intermediatePopulation
        for i in range(len(currentPopulation)):
            remainder = currentPopulation[i].Fitness - int(currentPopulation[i].Fitness)
            if (self.randomizer.uniform(self.MN,self.MX) < remainder):
                intermediatePopulation[i] = Genotype(currentPopulation[i].GetParameterCopy())
        
        return intermediatePopulation

# Only selects the best three genotypes of the current population and copies them to the intermediate population.
    def DefaultSelectionOperator(self, currentPopulation):
        intermediatePopulation = []
        intermediatePopulation.append(currentPopulation[0])
        intermediatePopulation.append(currentPopulation[1])
        intermediatePopulation.append(currentPopulation[2])

        return intermediatePopulation
    
#Recombination operator for the genetic algorithm, recombining random genotypes of the intermediate population
    def RandomRecombination(self, intermediatePopulation, newPopulationSize):
        if (len(intermediatePopulation) < 2):
            return intermediatePopulation

        newPopulation = []
        #Always add best two (unmodified)
        newPopulation.append(intermediatePopulation[0])
        newPopulation.append(intermediatePopulation[1])
        
        count = len(intermediatePopulation)
        while (len(newPopulation) < newPopulationSize):
            # Get two random indices that are not the same
            rand1 = self.randomizer.randint(0, count-1)
            rand2 = self.randomizer.randint(0, count-1)
            while (rand2 == rand1):
                rand2 = self.randomizer.randint(0, count-1)

            offspring1, offspring2 = self.CompleteCrossover(intermediatePopulation[rand1],
                                                            intermediatePopulation[rand2],
                                                            self.CrossSwapProb)
            newPopulation.append(offspring1)
            if (len(newPopulation) < newPopulationSize):
                newPopulation.append(offspring2)

        return newPopulation

# Simply crosses the first with the second genotype of the intermediate population until the new
# population is of desired size.
# "intermediatePopulation" -- The intermediate population that was created from the selection process
    def DefaultRecombinationOperator(self, intermediatePopulation, newPopulationSize):
        if (intermediatePopulation.Count < 2):
            return []

        newPopulation = []
        while (len(newPopulation) < newPopulationSize):
            offspring1, offspring2= self.CompleteCrossover(intermediatePopulation[0], 
                                                           intermediatePopulation[1], 
                                                           self.CrossSwapProb)
            newPopulation.append(offspring1)
            if (len(newPopulation) < newPopulationSize):
                newPopulation.append(offspring2)

        return newPopulation

    def CompleteCrossover(self, parent1, parent2, swapChance):
        # Initialise new parameter vectors
        parameterCount = parent1.GetCount()
        off1Parameters = [i for i in range(parameterCount)] 
        off2Parameters = [i for i in range(parameterCount)]
        # Iterate over all parameters randomly swapping
        #self.randomizer.seed()
        for i in range(parameterCount):
            if (self.randomizer.uniform(self.MN,self.MX) < swapChance):
                # Swap parameters
                off1Parameters[i] = parent2.parameters[i]
                off2Parameters[i] = parent1.parameters[i]
            else:
                # Don't swap parameters
                off1Parameters[i] = parent1.parameters[i]
                off2Parameters[i] = parent2.parameters[i]
                    
        offspring1 = Genotype(off1Parameters)
        offspring2 = Genotype(off2Parameters)
        return offspring1, offspring2

# Mutates all members of the new population with the default probability, while leaving the first 2 genotypes in the list untouched.
    def MutateAllButBestTwo(self, newPopulation):
        new_pop = newPopulation
        #self.randomizer.seed()
        for i in range(len(newPopulation)):
            if (self.randomizer.uniform(self.MN,self.MX) < self.MutationPerc):
                new_pop[i] = self.MutateGenotype(newPopulation[i], self.MutationProb, self.MutationAmount)
        return new_pop

# Simply mutates each genotype with the default mutation probability and amount.
    def DefaultMutationOperator(self, newPopulation):
        new_pop = newPopulation
        #self.randomizer.seed()
        for genotype in newPopulation:
            if (self.randomizer.uniform(self.MN,self.MX) < self.MutationPerc):
                new_pop.append(self.MutateGenotype(genotype, self.MutationProb, self.MutationAmount))
        return new_pop

# Mutates the given genotype by adding a random value in range [-mutationAmount, mutationAmount] 
# to each parameter with a probability of mutationProb
# "genotype" -- The parameters of genotype to be mutated
# "mutationProb" -- The probability of a parameter being mutated
# "mutationAmount" -- A parameter may be mutated by an amount in range [-mutationAmount, mutationAmount]
    def MutateGenotype(self, genotype, mutationProb, mutationAmount):
        gene = genotype
        #self.randomizer.seed()
        for i in range(genotype.GetCount()):
            if (self.randomizer.uniform(self.MN,self.MX) < mutationProb):
                gene.parameters[i] += self.randomizer.uniform(self.MN,self.MX)*(mutationAmount*2)-mutationAmount
        return gene