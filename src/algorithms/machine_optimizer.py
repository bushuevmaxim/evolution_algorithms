import copy
import random

import numpy as np
from algorithms.ant import Ant
from tqdm import tqdm


class MachineEvolution:
    def __init__(
        self,
        field,
        n_apples,
        n_states,
        cross_size,
        population_size,
        mutation_probability=0.7,
        cross_probability=0.6,
        forward_probability=0.9,
        max_steps=900
    ):

        self.n_states = n_states
        self.machines_population = []
        self.machines_population_results = []
        self.result_history = []
        self.best_machine = None
        self.field = field
        self.cross_size = cross_size
        self.population_size = population_size
        self.n_apples = n_apples
        self.max_steps = max_steps
        self.mutation_probability = mutation_probability

        self.cross_probability = cross_probability

        self.forward_probability = forward_probability

    def init_population(self):
        for i in range(self.population_size):
            machine = {0: [], 1: []}
            for j in range(self.n_states):
                machine[0].append(
                    [random.randint(0, 2), random.randint(
                        0, self.n_states - 1)]
                )
                machine[1].append(
                    [random.randint(0, 2), random.randint(
                        0, self.n_states - 1)]
                )
            self.machines_population.append(machine)

    def get_machine_result(self, machine):
        ant = Ant(self.n_apples, self.field.copy())
        state = 0

        used_states = []
        path = []

        for _ in range(self.max_steps):
            if state not in used_states:
                used_states.append(state)
            action, state = machine[1 if ant.check_apple() else 0][state]
            path.append(tuple(ant.coords.copy()))
            ant.move(action)

            if ant.terminal:
                break
        return ant.apples, path, used_states

    def get_population_results(self):
        results = []
        for machine in self.machines_population:
            apple, _, _ = self.get_machine_result(machine)
            results.append(apple)

        self.machines_population_results = results

    def generate_next_population(self):
        self.get_population_results()

        best_machine_idxs = np.argsort(self.machines_population_results)[
            ::-1][:self.cross_size]
        best_machines = [self.machines_population[i]
                         for i in best_machine_idxs]

        self.machines_population = best_machines
        while len(self.machines_population) < self.population_size:
            parent_machines = copy.deepcopy(
                random.sample(self.machines_population, 2))
            child_machines = self.cross(parent_machines)
            self.machines_population.extend(child_machines)

        if len(self.machines_population) > self.population_size:
            self.machines_population.pop()

        self.mutation()
        self.go_straight()

    def cross(self, machines):
        len_states = len(machines[0][0])

        for i in range(2):
            for state_idx in range(len_states):
                if random.random() < self.cross_probability:
                    machines[0][i][state_idx][0], machines[1][i][state_idx][0] = machines[1][i][state_idx][0], machines[0][i][state_idx][0]
                if random.random() < self.cross_probability:
                    machines[0][i][state_idx][1], machines[1][i][state_idx][1] = machines[1][i][state_idx][1], machines[0][i][state_idx][1]
        return machines


    def mutation(self):
        len_states = len(self.machines_population[0][0])
        for machine_idx in range(self.population_size):
            mutation_machine = copy.deepcopy(
                self.machines_population[machine_idx])
            for i in range(2):
                for state_idx in range(len_states):
                    if random.random() < self.mutation_probability:
                        mutation_machine[i][state_idx][1] = random.randint(
                            0, len_states - 1)
                    if random.random() < self.mutation_probability:
                        mutation_machine[i][state_idx][0] = random.randint(
                            0, 2)

            mutation_result, _, _ = self.get_machine_result(mutation_machine)

            if mutation_result > self.machines_population_results[machine_idx]:
                self.machines_population[machine_idx] = mutation_machine
                self.machines_population_results[machine_idx] = mutation_result

    def go_straight(self):
        len_states = len(self.machines_population[0][0])
        for machine_idx in range(self.population_size):
            mutation_machine = copy.deepcopy(
                self.machines_population[machine_idx])
            for state_idx in range(len_states):
                if random.random() < self.forward_probability:
                    mutation_machine[1][state_idx][0] = 0

            mutation_result, _, _ = self.get_machine_result(mutation_machine)

            if mutation_result > self.machines_population_results[machine_idx]:
                self.machines_population[machine_idx] = mutation_machine
                self.machines_population_results[machine_idx] = mutation_result

    def run(self, n_epoh):
        self.init_population()
        self.get_population_results()
        self.result_history.append(max(self.machines_population_results))
        for _ in tqdm(range(n_epoh)):
            self.generate_next_population()
            index_best = np.argmax(self.machines_population_results)
            self.result_history.append(
                self.machines_population_results[index_best])
            self.best_machine = self.machines_population[index_best]
