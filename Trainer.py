from TheCar import Car
from Sensors import Sensors
from Track import Track
import torch
from genetic.geneticNN import GeneticNN

# Trainer of NNet for car racing
class NTrainer:
    def __init__(self):
        self.Track = Track()
        self.Cars = []
        self.MaxIterations = 5000
        self.iteration = 0
        self.DefaultNNWeights = []
        self.Generation = 0
        self.GeneticNN =  None
        self.Population = 60
        self.Sensors = Sensors()

    def IsAlive(self):
        for car in self.Cars:
            if (car.IsAlive):
                return True

        return False
    
    def BuildFirstPopulation(self, file = ''):
        self.Cars.clear()
        self.Generation = 0

        # GeneticNN = [6, 5, 4, 3, 3 ], Population
        self.GeneticNN = GeneticNN( [6, 6, 6, 3], self.Population) # - best topology
        self.GeneticNN.CrossSwapProb = 0.2
        self.GeneticNN.MutationProb = 0.3
        self.GeneticNN.MutationAmount = 2
        self.GeneticNN.MutationPerc = 0.8

        # загрузка весов по умолчанию из файла 
        if file != '':
            self.GeneticNN.GetNN(0).LoadWeights(file)
        
        for i in range(self.GeneticNN.PopulationCount):
            car = Car(i)
            # load default weights
            #if file != '':
                #self.GeneticNN.GetNN(i).SetWeights(self.GeneticNN.GetNN(0).GetWeights())  
            #else:
                #self.GeneticNN.GetNN(i).SetRandomWeights(-1000.0,1000.0)
            self.Cars.append(car)
            car.Reset(self.Track, False)

    def Update(self, dt):
        self.iteration+=1
        for i in range(self.GeneticNN.PopulationCount):
            car = self.Cars[i]
            self.UpdateCar(car, dt)
            if (car.IsOutOfTrack):
                car.IsAlive = False
            if (self.iteration>self.MaxIterations and (car.TotalPassedLength/self.iteration<0.1)):
                car.IsAlive = False

    def UpdateCar(self, car, dt):
        sensors = [i for i in range(self.GeneticNN.GetNN(car.Index).Layers[0].NeuronCount)]
        sensors = self.Sensors.GetDistances(car, self.Track, sensors, 0)
        sensors[5] = car.Velocity.Length()
        output = self.GeneticNN.GetNN(car.Index).ProcessInputs(sensors)
        steering = output[1]

        car.Update(self.Track, 1, steering, output[2] > 0, dt)

    def BuildNextGeneration(self):
        # SetEvaluation
        for i in range(self.GeneticNN.PopulationCount):
            self.GeneticNN.SetEvaluation(i, self.Cars[i].TotalPassedLength - self.Cars[i].Penalty)
        # BuildNextGeneration
        self.GeneticNN.BuildNextGeneration()
        # set random Adhesion
        self.Track.Adhesion = 1
        # reset cars
        for ii in range (len(self.Cars)):
            self.Cars[ii].Reset(self.Track, False)
        self.iteration = 0
        self.Generation+=1

    def find_leader(self):
        maxTotalPath = 0.0
        leader = Car(0)
        for car in self.Cars:
            if (car.TotalPassedLength > maxTotalPath):
                maxTotalPath = car.TotalPassedLength
                if(car.IsAlive):
                    leader = car
        return leader
        
    def Run(self, generationCount):
        self.BuildFirstPopulation()
        self.BuildNextGeneration()

        while (True):
            if (not self.IsAlive()):
                if (self.Generation >= generationCount):
                    break
                self.BuildNextGeneration()
            
            dt = 0.02
            # update cars
            self.Update(dt)
