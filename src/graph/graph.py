from abc import ABC, abstractmethod


class Graph(ABC):

    @abstractmethod
    def get_view_graph(self):
        pass

    @abstractmethod
    def get_random_path(self):
        pass

    @abstractmethod
    def edge_exists(self, src: int, dst: int):
        pass

    @abstractmethod
    def get_path_score(self, path):
        pass
