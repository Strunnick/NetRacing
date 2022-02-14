import random
#from . import neurallayer
from .neurallayer import NeuralLayer, ActivationFunctionType

# Class representing one genotype of a population
class Genotype: 
# Instance of a new genotype with given parameter vector and initial fitness of 0
# The parameter vector to initialise this genotype with
    def __init__(self, parameters):
        self.parameters = parameters
        self.Fitness = 0
        self.Evaluation = 0
        self.randomizer = random
        self.Count = len(parameters)
        
    def GetCount(self):
        return len(self.parameters)

# Compares this genotype with another genotype depending on their fitness values.
# "other" -- The genotype to compare this genotype with
# <returns> -- The result of comparing the two floating point values representing 
# the genotypes fitness in reverse order
    def CompareTo(self, other):
        if(other.Fitness > self.Fitness): 
            return other.Fitness
        else: 
            return self.Fitness #in reverse order for larger fitness being first in list

# Sets the parameters of this genotype to random values in given range.
    def SetRandomParameters(self, minValue, maxValue):
        self.randomizer.seed()
        # Check arguments
        if (minValue > maxValue): 
            print("Minimum value may not exceed maximum value")
        # Generate random parameter vector
        rrange = maxValue - minValue
        for i in range(self.GetCount()):
            self.parameters[i] = (self.randomizer.uniform(-1000000000.0,1000000000.0) * rrange) + minValue

# Returns a copy of the parameter vector.
    def GetParameterCopy(self):
        return self.parameters

# Saves the parameters of this genotype to a file at given file path.
    def SaveToFile(self, filePath):
        f = open(filePath)
        for param in self.parameters:
            f.write( str(param) + ";" )

# Generates a random genotype with parameters in given range.
    def GenerateRandom(parameterCount, minValue, maxValue):
        # Check arguments
        if (parameterCount == 0): return Genotype([0.0])
        randomGenotype = Genotype([parameterCount])
        randomGenotype.SetRandomParameters(minValue, maxValue)

        return randomGenotype
    
# Loads a genotype from a file with given file path.
    def LoadFromFile(self, filePath):
        f = open(filePath)
        parameters = []
        paramStrings = f.split(';')
        for parameter in paramStrings:
            if (not float(parameter)):
                print("The file at given file path does not contain a valid genotype serialisation")
            parameters.append(float(parameter))

        return Genotype(parameters)