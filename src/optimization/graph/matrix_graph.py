from src.optimization.graph.graph import Graph
import numpy as np


class MatrixGraph(Graph):

    def __init__(self, matrix_adjacency: np.ndarray):
        self.matrix_adjacency = matrix_adjacency
        self.n = matrix_adjacency.shape[0]

    def get_view_graph(self):
        print('Матрица смежности')
        return self.matrix_adjacency

    def get_random_path(self):
        start_town = np.random.randint(0, self.n - 1)

        path = [start_town]
        while True:
            current_town = start_town
            for i in range(self.n - 1):
                min_town_dist = np.inf
                for j in range(self.n):
                    if self.matrix_adjacency[current_town][j] == 0:
                        continue
                    if j in path:
                        continue
                    if self.matrix_adjacency[current_town][j] < min_town_dist:
                        min_town_dist = self.matrix_adjacency[current_town][j]
                        town = j
                path.append(town)
                current_town = town
            if self.edge_exists(path[-1], start_town):
                break
            else:
                start_town = np.random.randint(0, self.n - 1)
                path = [start_town]

        return np.array(path)

    def edge_exists(self, i: int, j: int):
        return self.matrix_adjacency[i][j] != 0

    def get_path_score(self, path: np.ndarray):
        n = path.shape[0]
        score = 0
        for i in range(n - 1):
            src = path[i]
            dst = path[i + 1]
            weight = self.matrix_adjacency[src][dst]
            score += weight
        score += self.matrix_adjacency[path[-1]][path[0]]
        return score
