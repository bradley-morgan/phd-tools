import numpy as np


class MUniform:

    def __init__(self, probabiltiy):
        self.probability = probabiltiy

    def __call__(self, dna):

        for i in range(len(dna)):
            gene = dna[i]
            rand = np.random.uniform(0, 1)
            # if in probability range then flip bit
            if rand < self.probability:
                dna[i] = gene ^ 1

        return dna
