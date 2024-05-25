import numpy as np
from machine_optimizer import MachineEvolution
from matplotlib import pyplot as plt


def main():
    map = np.zeros((32, 32), dtype=int)
    for i in range(90):
        while True:
            x = np.random.randint(0, 32)
            y = np.random.randint(0, 32)
            if map[x, y] != 1:
                map[x, y] = 1
                break
    print(np.sum(map))

    alg = MachineEvolution(100, 5, 100)
    alg.set_map(map)
    alg.run(100)
    history = alg.result_history
    plt.plot(history)
    plt.show()


main()