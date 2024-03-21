from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def update_best_solution(self):
        pass

    @abstractmethod
    def get_best_solution(self):
        pass
