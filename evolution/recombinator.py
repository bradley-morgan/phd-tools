import numpy as np


class RUniform:

    def __init__(self, probability=0.5):
        self.probability = probability

    def __call__(self, dna1, dna2):

        # if greater than self.probability then take parent 1 dna else take parent 2
        rand = np.random.uniform(0, 1)
        child = np.zeros(shape=(len(dna1)))

        for i in range(len(child)):
            if rand > self.probability:
                child[i] = dna1[i]
            else:
                child[i] = dna2[i]

        return child