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
        #self.Layers = [0 for i in range(len(topology)-1)] # NeuralLayer(topology.Length - 1)
        for i in range(len(topology)-1):
            #self.Layers[i] = NeuralLayer(topology[i], topology[i + 1])
            #self.Layers[i].NeuronActivationFunctionType = activationFunction
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
            #c0 = layer.Weights.GetLength(0)
            #c1 = layer.Weights.GetLength(1)
            #Loop over all nodes of current layer
            for i in range(len(layer.Weights)):
                for j in range(len(layer.Weights[i])):
                #Loop over all nodes of next layer
                    layer.Weights[i][j] = weights[ iWeight ]
                    iWeight += 1

    def GetWeights(self):
        #weights = [0 in range(self.WeightCount)]
        weights = []
        #iWeight = 0
        # Loop over all layers
        for layer in self.Layers:
            #Loop over all nodes of current layer
            for i in range(len(layer.Weights)):
                for j in range(len(layer.Weights[i])):
                    #Loop over all nodes of next layer
                    #iWeight+= 1
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
        # save to file
        f = open(file, 'w')
        # version
        f.write(byte(0))
        # number of layers - int32?
        f.write(len(self.Layers))
        for i in range (len(self.Topology)):
            f.write(self.Topology[i])
        for w in self.GetWeights():
            f.write(w)
        f.close()

    def LoadWeightsSafe(self, file):
        self.SetRandomWeights(1,100)
        '''
        f = open(file, 'w')
        # version
        f.read(byte())
        # number of layers
        layerCount = f.read(int())
        # topology
        topology = [layerCount + 1]
        for i in range(len( topology )):
            topology[i] = f.read(int())
        # weight count
        weightCount = 0
        for (var i = 0; i < topology.Length - 1; i++)
            weightCount += (topology[i] + 1) * topology[i + 1];

        # read weights
            var counter = 0;
            for (var iLayer = 0; iLayer < layerCount; iLayer++)
            {
                var c0 = topology[iLayer] + 1;
                var c1 = topology[iLayer + 1];
                for (var i = 0; i < c0; i++) //Loop over all nodes of current layer
                for (var j = 0; j < c1; j++) //Loop over all nodes of next layer
                {
                    var w = bw.ReadSingle();
                    counter++;

                    if (iLayer < Layers.Length)
                    {
                        var layer = Layers[iLayer];
                        if (i < layer.Weights.GetLength(0) && j < layer.Weights.GetLength(1))
                            if (i == c0 - 1) //bias ?
                                layer.Weights[layer.Weights.GetLength(0) - 1, j] = w;
                            else
                                layer.Weights[i, j] = w;'''
