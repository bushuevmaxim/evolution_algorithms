import copy
import random

import numpy as np
from algorithms.ant import Ant
from tqdm import tqdm


class MachineEvolution:
    def __init__(self, init_n_states,
                 cross_size,
                 population_size,
                 mutation_probability=0.7,
                 cross_probability=0.6,
                 go_straight_chance=0.9,
                 min_n_states=30,
                 max_steps=900,):

        self.init_n_states = init_n_states
        self.machines_population = []
        self.machines_population_results = []
        self.result_history = []
        self.best_machine = None
        self.map = None
        self.cross_size = cross_size
        self.population_size = population_size
        self.ant = Ant()
        self.max_steps = max_steps

        self.mutation_probability = mutation_probability

        self.cross_probability = cross_probability

        self.go_straight_chance = go_straight_chance
        self.min_n_states = min_n_states

    def init_population(self):
        for i in range(self.population_size):
            machine = {0: [], 1: []}
            for j in range(self.init_n_states):
                machine[0].append(
                    [random.randint(0, 2), random.randint(
                        0, self.init_n_states - 1)]
                )
                machine[1].append(
                    [random.randint(0, 2), random.randint(
                        0, self.init_n_states - 1)]
                )
            self.machines_population.append(machine)

    def get_machine_result(self, machine):
        self.ant.reset_ant(self.map)
        state = 0

        used_states = []
        path = []

        for step in range(self.max_steps):
            if state not in used_states:
                used_states.append(state)
            action, state = machine[1 if self.ant.check_fruit() else 0][state]
            path.append(tuple(self.ant.coords.copy()))
            self.ant.move(action)

            if self.ant.terminal:
                break
        return self.ant.fruits, path, used_states

    def get_population_results(self):
        results = []
        for machine in self.machines_population:
            fruit, _, _ = self.get_machine_result(machine)
            results.append(fruit)

        self.machines_population_results = results

    def generate_next_population(self):
        self.get_population_results()

        best_machine_idxs = np.argsort(self.machines_population_results)[
            ::-1][:self.cross_size]
        best_machines = [self.machines_population[i]
                         for i in best_machine_idxs]

        if len(best_machines[0][0]) >= self.min_n_states:
            fix_best_machines = self.fix_unusable_state(best_machines)
            self.machines_population = fix_best_machines
        else:
            self.machines_population = best_machines
        while len(self.machines_population) < self.population_size:
            parent_machines = copy.deepcopy(
                random.sample(self.machines_population, 2))
            child_machines = self.cross(parent_machines)
            self.machines_population.extend(child_machines)

        if len(self.machines_population) > self.population_size:
            self.machines_population.pop()

        self.default_mutation()
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

    def set_map(self, map):
        self.map = map

    def default_mutation(self):
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

    def fix_unusable_state(self, best_machines):
        max_len_states = self.min_n_states
        for machine in best_machines:
            _,_, used_states = self.get_machine_result(machine)
            len_states = len(machine[0])

            # удаление лишних состояний
            for i in range(2):
                for state_idx in range(len_states):
                    if machine[i][state_idx][1] not in used_states:
                        machine[i][state_idx][1] = 0

            for i in range(len_states - 1, -1, -1):
                if i not in used_states:
                    del machine[0][i]
                    del machine[1][i]
                    for j in range(len(machine[0])):
                        if machine[0][j][1] > i:
                            machine[0][j][1] -= 1
                        if machine[1][j][1] > i:
                            machine[1][j][1] -= 1
                    i -= 1

            len_states = len(machine[0])

            if max_len_states < len_states:
                max_len_states = len_states

        for machine in best_machines:
            while len(machine[0]) != max_len_states:
                machine[0].append([random.randint(0, 2), 0])
                machine[1].append([random.randint(0, 2), 0])

        return best_machines

    def go_straight(self):
        len_states = len(self.machines_population[0][0])
        for machine_idx in range(self.population_size):
            mutation_machine = copy.deepcopy(
                self.machines_population[machine_idx])
            for state_idx in range(len_states):
                if random.random() < self.go_straight_chance:
                    mutation_machine[1][state_idx][0] = 0

            mutation_result, _, _ = self.get_machine_result(mutation_machine)

            if mutation_result > self.machines_population_results[machine_idx]:
                self.machines_population[machine_idx] = mutation_machine
                self.machines_population_results[machine_idx] = mutation_result

    def run(self, n_epoh):
        self.init_population()
        self.get_population_results()
        self.result_history.append(max(self.machines_population_results))
        for i in tqdm(range(n_epoh)):
            self.generate_next_population()
            index_best = np.argmax(self.machines_population_results)
            self.result_history.append(self.machines_population_results[index_best])
            self.best_machine = self.machines_population[index_best]
