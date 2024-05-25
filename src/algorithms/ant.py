

class Ant:
    def __init__(self):
        self.map_size = 32
        self.max_fruits = 90

    def reset_ant(self, map):
        self.set_map(map)
        self.coords = [0, 0]
        self.last_path = []
        self.direction = 1 # по часовй стрелке, 0 - вверх
        self.fruits = 0
        self.max_fruits = 90
        self.terminal = False
        self.see_fruit = False

    def set_map(self, map):
        self.map = map.copy()

    def move(self, action: int):

        # 0 - прямо, 1 - направо, 2 - налево
        if action == 0:
            if self.direction == 0:
                self.coords[1] = (self.coords[1] + 1) % self.map_size

            elif self.direction == 1:
                self.coords[0] = (self.coords[0] + 1) % self.map_size

            elif self.direction == 2:
                self.coords[1] = (self.coords[1] - 1) % self.map_size

            else:
                self.coords[0] = (self.coords[0] - 1) % self.map_size

            if self.map[self.coords[0], self.coords[1]] == 1:
                self.map[self.coords[0], self.coords[1]] = 0
                self.max_fruits -= 1
                self.fruits += 1

            if self.max_fruits == 0:
                self.terminal = True

        elif action == 1:
            self.direction = (self.direction + 1) % 4
        elif action == 2:
            self.direction = (self.direction - 1) % 4

    def check_fruit(self):
        if self.direction in [0, 2]:
            if self.map[self.coords[0], (self.coords[1] - self.direction + 1) % self.map_size] == 1:
                self.see_fruit = True
            else:
                self.see_fruit = False
        else:
            if self.map[(self.coords[0] + 2 - self.direction) % self.map_size, self.coords[1]] == 1:
                self.see_fruit = True
            else:
                self.see_fruit = False
        return self.see_fruit