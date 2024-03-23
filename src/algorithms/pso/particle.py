import numpy as np

from algorithms.pso.velocity import Velocity


class Particle:

    def __init__(self, solution: np.ndarray, score: int):
        self.current_solution = solution
        self.solutions = []
        self.best_solution = solution
        self.current_score = score
        self.best_score = score
        self.velocity = Velocity(np.zeros(solution.shape))

    def update_best_solution(self, solution):
        self.best_solution = solution

    def update_velocity(self, velocity):
        self.velocity = velocity

    def clear_velocity(self):
        self.velocity = Velocity(np.zeros(self.current_solution.shape))

    def update_current_solution(self, solution):
        self.current_solution = solution

    def update_best_score(self, score):
        self.best_score = score

    def update_current_score(self, score):
        self.current_score = score
