import numpy as np


class Velocity:
    def __init__(self, vector: np.ndarray):
        self.vector = vector

    def get_vector(self) -> np.ndarray:
        return self.vector

    def __add__(self, o):
        vector = o.vector + self.vector
        vector[vector > 1] = 0
        return vector

    def __setitem__(self, key, value):
        if value > 1 or value < 0:
            raise Exception('Try set invalid value')
        self.vector[key] = value

    def __getitem__(self, key):
        return self.vector[key]

    def __len__(self):
        return len(self.vector)
