import numpy as np


class Poly:
    def __init__(self, n):
        self.deg = -1
        self.coeff = np.zeros(n)
        self.size = n

    def clear(self):
        self.coeff = self.coeff * 0

    def zero(self):
        self.deg = -1
        self.coeff = self.coeff * 0

