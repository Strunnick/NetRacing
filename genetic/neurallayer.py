from enum import Enum
import random, sys, math

# Class representing a single layer of a fully connected feedforward neural network.
class NeuralLayer:
## Initialises a new neural layer for a fully connected feedforward neural network with given
## amount of node and with connections to the given amount of nodes of the next layer
## "nodeCount" -- The amount of nodes in this layer
##" outputCount" -- The amount of nodes in the next layer
## All weights of the connections from this layer to the next are initialised with the default double value
    def __init__(self, nodeCount, outputCount):
#   The weights of the connections of this layer to the next layer.
#   E.g., weight [i, j] is the weight of the connection from the i-th weight
#   of this layer to the j-th weight of the next layer
        self.Weights =[[x for x in range(outputCount)] for n in range(nodeCount+1)] #  1 for bias node
        self.randomizer = random
        #The default activation function is the sigmoid function
        self.NeuronActivationFunctionType = ActivationFunctionType.SigmoidFunction
# The amount of neurons in this layer.
        self.NeuronCount = nodeCount
# The amount of neurons this layer is connected to, i.e., the amount of neurons of the next layer.
        self.OutputCount = outputCount
        # diapason for random
        self.MN = -1000.0
        self.MX = 1000.0
    
# Processes the given inputs using the current weights to the next layer
# "inputs" -- The inputs to be processed
# returns -- The calculated outputs
    def ProcessInputs(self, inputs):
        # Check arguments
        if (len(inputs) != self.NeuronCount):
            print("Given xValues do not match layer input count")

        # Calculate sum for each neuron from weighted inputs and bias
        sums = [i for i in range(self.OutputCount)]
        for j in range(self.OutputCount):
            ssum = 0.0
            for i in range (len(inputs)):
                ssum += inputs[i] * self.Weights[i][j]
            # Add bias (always on) neuron to inputs
            ssum += 1 * self.Weights[self.NeuronCount][j]
            sums[j] = ssum

        # Apply activation function to sum
        if (self.NeuronActivationFunctionType == ActivationFunctionType.SigmoidFunction):
            for i in range (len(sums)):
                sums[i] = self.SigmoidFunction(sums[i])
        if (self.NeuronActivationFunctionType == ActivationFunctionType.TanHFunction):
            for i in range (len(sums)):
                sums[i] = self.TanHFunction(sums[i])
        if (self.NeuronActivationFunctionType == ActivationFunctionType.SoftSignFunction):
            for i in range (len(sums)):
                sums[i] = self.SoftSignFunction(sums[i])
        #if (self.NeuronActivationFunctionType == ActivationFunctionType.Identity):
                # pass
        return sums

# Copies this NeuralLayer including its weights
# return -- A deep copy of this NeuralLayer
    def DeepCopy(self):
        # Copy weights
        copiedWeights = [[len(self.Weights[0])] for n in range(len(self.Weights))]
        for x in range(len(self.Weights)):
            for y in range(len(self.Weights[0])):
                copiedWeights[x][y] = self.Weights[x][y]

        # Create copy
        newLayer = NeuralLayer(self.NeuronCount, self.OutputCount)
        newLayer.Weights = copiedWeights
        newLayer.NeuronActivationFunctionType = self.NeuronActivationFunctionType

        return newLayer

# Sets the weights of the connection from this layer to the next to random values in given range.
    def SetRandomWeights(self, minValue, maxValue):
        rrange = abs(minValue - maxValue)
        for i in range(len(self.Weights)):
            for j in range(len(self.Weights[i])):
                self.randomizer.seed()
                self.Weights[i][j] = minValue + (self.randomizer.uniform(self.MN,self.MX) * rrange)

# Returns a string representing this layer's connection weights.
    def __str__(self):
        output = ""
        for x in range(len(self.Weights)):
            for y in range(len(self.Weights[0])):
                output += "[" + x + "," + y + "]: " + self.Weights[x][y]
            output += "\n"

        return output

# The standard sigmoid function
    def SigmoidFunction(self, xValue):
        if (xValue > 10): return 1.0
        if (xValue < -10): return 0.0
        return 1.0 / (1.0 + math.exp(-xValue))

    def TanHFunction(self, xValue):
        if (xValue > 10): return 1.0
        if (xValue < -10): return -1.0
        return math.tanh(xValue)

    def SoftSignFunction(self, xValue):
        return xValue / (1 + abs(xValue))

class ActivationFunctionType(Enum):
    Identity = 1
    SigmoidFunction = 2
    TanHFunction = 3
    SoftSignFunction = 4
