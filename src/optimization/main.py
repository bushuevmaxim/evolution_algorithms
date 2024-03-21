import numpy as np

from algorithms.pso.pso import ParticlesSwarm
from graph.matrix_graph import MatrixGraph

if __name__ == "__main__":
    matrix_new = []
    with open('src/optimization/matrix.txt') as f:
        lines = f.readlines()
        for line in lines:
            matrix_new.append(list(map(int, line.split(' '))))

    graph_new = MatrixGraph(np.array(matrix_new))
    particlesSwarm = ParticlesSwarm(graph_new, 200, 150, 0.7, 1)
    particlesSwarm.execute()
    best_particle = particlesSwarm.get_best_solution()
    print(best_particle.best_solution)
    print(best_particle.best_score)
4
