#from . import neurallayer
from .neurallayer import NeuralLayer, ActivationFunctionType

# Class representing a fully connected feedforward neural network.
class NeuralNetwork:
# Initialises a new fully connected feedforward neural network with given topology.
# out: An array of unsigned integers representing the node count of each layer from input to output layer
    def __init__(self, activationFunction, topology):
        # An array of unsigned integers representing the node count
        # of each layer of the network from input to output layer
        self.Topology = topology
        # The amount of overall weights of the connections of this network
        # Calculate overall weight count
        self.WeightCount = 0
        for i in range(len(topology)-1):
            self.WeightCount += int((topology[i] + 1) * topology[i + 1]) # + 1 for bias node
        # The individual neural layers of this network
        # Initialise layers
        self.Layers = []
        for i in range(len(topology)-1):
            l = NeuralLayer(topology[i], topology[i + 1])
            l.NeuronActivationFunctionType = activationFunction
            self.Layers.append(l)
            del(l)

    # Processes the given inputs using the current network's weights
    # returns - The calculated outputs
    def ProcessInputs(self, inputs):
        # Check arguments
        if (len(inputs) != self.Layers[0].NeuronCount):
            print("Given inputs - {0} do not match network input - {1} amount".format(self.Layers[0].NeuronCount, len(inputs)))
        # Process inputs by propagating values through all layers
        outputs = inputs
        for layer in self.Layers:
            outputs = layer.ProcessInputs(outputs)

        return outputs

    def SetWeights(self, weights):
        #Check if topology is valid
        if (self.WeightCount != len(weights)):
            print("Given genotype's parameter count must match the NN topology's weight count")

        iWeight = 0
        # Loop over all layers
        for layer in self.Layers:
            #Loop over all nodes of current layer
            for i in range(len(layer.Weights)):
                for j in range(len(layer.Weights[i])):
                #Loop over all nodes of next layer
                    layer.Weights[i][j] = weights[ iWeight ]
                    iWeight += 1

    def GetWeights(self):
        weights = []
        # Loop over all layers
        for layer in self.Layers:
            #Loop over all nodes of current layer
            for i in range(len(layer.Weights)):
                for j in range(len(layer.Weights[i])):
                    #Loop over all nodes of next layer
                    weights.append(layer.Weights[i][j])
        return weights

    # Sets the weights of this network to random values in given range.
    def SetRandomWeights(self, minValue, maxValue):
        if (self.Layers != None):
            for layer in self.Layers:
                layer.SetRandomWeights(minValue, maxValue)

    # Returns a new NeuralNetwork instance with the same topology and
    # activation functions, but the weights set to their default value.
    def GetTopologyCopy(self):
        copy = NeuralNetwork(ActivationFunctionType.Identity, self.Topology)
        for i in range(len(self.Layers)):
            copy.Layers[i].NeuronActivationFunctionType = self.Layers[i].NeuronActivationFunctionType
        return copy


    # Copies this NeuralNetwork including its topology and weights
    # returns -- A deep copy of this NeuralNetwork
    def DeepCopy(self):
        newNet = NeuralNetwork(ActivationFunctionType.Identity, self.Topology)
        for i in range(len(self.Layers)):
            newNet.Layers[i] = self.Layers[i].DeepCopy()
        return newNet

    # Returns a string representing this network in layer order
    def __str__(self):
        output = ""
        for i in range(len(self.Layers)):
            output += "Layer " + i + ":\n" + str(self.Layers[i])
        return output
    
    def SaveWeights(self, file):
        with open(file, "w") as f:
            # version
            print(0, file = f)
            # number of layers - int32?
            print(len(self.Layers), file = f)
            
            for i in range (len(self.Topology)):
                print(self.Topology[i], file = f)
            for w in self.GetWeights():
                print(w, file = f)
            f.close()

    def LoadWeights(self, file):
        f = open(file, 'r')
        l = [float(line.strip()) for line in f]
        self.SetWeights(l)
            
    def LoadWeightsSafe(self, file):
        f = open(file, 'r')
        l = [line.strip() for line in f]
        f.close()
        # l[0] - version
        # number of layers
        layerCount = int(l[1])
        # topology
        topology = [i for i in range(layerCount + 1)]
        for i in range(len( topology )):
            topology[i] = int(l[i+2])
        self.Topology = topology
        # create Layers
        # очистить список слоёв перед добавлением
        self.Layers.clear()
        for i in range(len(topology)-1):
            lay = NeuralLayer(topology[i], topology[i + 1])
            self.Layers.append(lay)
            del(lay)
        # read weights
        counter = 2 + len( topology ) # 6
        for iL in range(layerCount-1):
            c0 = topology[iL] + 1
            c1 = topology[iL + 1]
             #Loop over all nodes of current layer
            for i in range(c0):
                #Loop over all nodes of next layer
                for j in range(c1):
                    w = float(l[counter])
                    counter+= 1
                    if iL < len(self.Layers):
                        if (i < len(self.Layers[iL].Weights) and j < len(self.Layers[iL].Weights[0])):
                            # bias ?
                            if (i == c0 - 1): 
                                self.Layers[iL].Weights[ len(self.Layers[iL].Weights) - 1 ] [j] = w
                            else:
                                self.Layers[iL].Weights[i] [j] = w
        