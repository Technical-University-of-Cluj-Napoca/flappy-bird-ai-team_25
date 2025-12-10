import math
import random

class Perceptron:
    def __init__(self, weights=None):
        if weights:
            self.weights = weights
        else:
            self.weights = [random.uniform(-1, 1) for _ in range(4)]
        self.fitness = 0

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def predict(self, inputs):
        all_inputs = inputs + [1] 
        weighted_sum = 0
        for i, val in enumerate(all_inputs):
            weighted_sum += val * self.weights[i]
        return self.sigmoid(weighted_sum)
