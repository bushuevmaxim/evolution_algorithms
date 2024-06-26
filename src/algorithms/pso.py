import numpy as np
from algorithms.algorithm import Algorithm
from graph.graph import Graph

from .particle import Particle
from .velocity import Velocity


class ParticlesSwarm(Algorithm):
    def __init__(self, graph: Graph, n_iterations, n_particles, threshold: float = 0.7,
                 percent_global_scope: float = 0.2):
        self.graph = graph
        self.n_iterations = n_iterations
        self.particles = []
        self.n_particles = n_particles
        self.threshold = threshold

        self.sigma = int(percent_global_scope * n_particles)
        self.percent_global_scope = percent_global_scope
        self.best_solutions = []
        self.best_scores = []
        self.initialize()

    def initialize(self):
        for _ in range(self.n_particles):
            random_path = self.graph.get_random_path()
            score = self.graph.get_path_score(random_path)
            particle = Particle(random_path, score)
            self.particles.append(particle)

    def _update_velocity(self, particle: Particle, best_particle: Particle):
        n = len(particle.velocity)
        velocity = Velocity(np.zeros(n))
        particle_current_solution = particle.current_solution
        particle_best_solution = particle.best_solution

        global_best_solution = best_particle.best_solution

        for i in range(n):
            if particle_current_solution[i] != particle_best_solution[i]:
                phi = np.random.rand()
                if phi > self.threshold:
                    velocity[i] = 1
                else:
                    velocity[i] = 0
            if particle_current_solution[i] != global_best_solution[i]:
                phi = np.random.rand()
                if phi > self.threshold:
                    velocity[i] = 1
                else:
                    velocity[i] = 0
        particle.update_velocity(particle.velocity + velocity)

    def _update_particle(self, particle: Particle, best_solution: np.ndarray, epoch):
        velocity = particle.velocity
        n = len(velocity)

        particle_current_solution = np.copy(particle.current_solution)
        for source_index in range(n):
            if velocity[source_index] == 1:
                source = particle_current_solution[source_index]
                destination = best_solution[source_index]
                destination_index = np.where(
                    particle_current_solution == destination)[0][0]

                if source_index - 1 > 0 and not self.graph.edge_exists(particle_current_solution[source_index - 1],
                                                                       destination):
                    continue
                if source_index + 1 <= n - 1 and not self.graph.edge_exists(destination, particle_current_solution[
                        source_index + 1]):
                    continue
                if destination_index - 1 > 0 and not self.graph.edge_exists(
                        particle_current_solution[destination_index - 1], source):
                    continue
                if destination_index + 1 <= n - 1 and not self.graph.edge_exists(source, particle_current_solution[
                        destination_index + 1]):
                    continue

                if source_index == n - 1 and not self.graph.edge_exists(particle_current_solution[destination_index],
                                                                        particle_current_solution[0]):
                    continue

                if destination_index == n - 1 and not self.graph.edge_exists(particle_current_solution[source_index],
                                                                             particle_current_solution[0]):
                    continue
                particle_current_solution[source_index] = particle_current_solution[destination_index]
                particle_current_solution[destination_index] = source
        particle.update_current_solution(particle_current_solution)
        score = self.graph.get_path_score(particle_current_solution)
        particle.update_current_score(score)

        if list(particle_current_solution) not in particle.solutions:
            particle.solutions.append((epoch, list(
                particle_current_solution), score))

    def execute(self):
        global_best_particle = min(
            self.particles, key=lambda particle: particle.best_score)
        self.update_best_solution(global_best_particle
                                  )
        self.best_solutions.append((0,

                                    global_best_particle.best_solution, global_best_particle.best_score))
        for epoch in range(self.n_iterations):

            for current_particle in self.particles:
                current_particle.clear_velocity()
                if self.percent_global_scope < 1:
                    close_particles = sorted(self.particles, key=lambda particle: np.linalg.norm(
                        current_particle.best_solution - particle.best_solution))
                    best_particle = min(
                        close_particles[:self.sigma], key=lambda particle: particle.best_score)
                else:
                    best_particle = min(
                        self.particles, key=lambda particle: particle.best_score)

                best_solution = best_particle.best_solution
                self._update_velocity(current_particle, best_particle)

                self._update_particle(current_particle, best_solution, epoch)

                if current_particle.current_score < current_particle.best_score:
                    current_particle.update_best_solution(
                        current_particle.current_solution)
                    current_particle.update_best_score(
                        current_particle.current_score)

                if current_particle.best_score < global_best_particle.best_score:
                    self.update_best_solution(current_particle)
                    global_best_particle = current_particle
                    self.best_solutions.append((epoch,

                                                global_best_particle.best_solution, global_best_particle.best_score))
                if best_particle.best_score < global_best_particle.best_score:
                    self.update_best_solution(best_particle)
                    global_best_particle = best_particle
                    self.best_solutions.append(
                        (epoch, global_best_particle.best_solution, global_best_particle.best_score))

        return self.get_best_solution(), self.best_solutions

    def update_best_solution(self, particle):
        self.best_particle = particle

    def get_best_solution(self) -> Particle:
        return self.best_particle
