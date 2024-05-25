

class Ant:
    def __init__(self, n_apples, field):
        self.field_size = 32
        self.n_apples = n_apples
        self.field = field
        self.coords = [0, 0]
        self.direction = 1 # по часовой стрелке, 1 - смотрит вправо изначально
        self.apples = 0
        self.terminal = False

        

    def move(self, action: int):

        # 0 - прямо, 1 - направо, 2 - налево
        if action == 0:
            if self.direction == 0:
                self.coords[1] = (self.coords[1] + 1) % self.field_size

            elif self.direction == 1:
                self.coords[0] = (self.coords[0] + 1) % self.field_size

            elif self.direction == 2:
                self.coords[1] = (self.coords[1] - 1) % self.field_size

            else:
                self.coords[0] = (self.coords[0] - 1) % self.field_size

            if self.field[self.coords[0], self.coords[1]] == 1:
                self.field[self.coords[0], self.coords[1]] = 0
                self.n_apples -= 1
                self.apples += 1

            if self.n_apples == 0:
                self.terminal = True

        elif action == 1:
            self.direction = (self.direction + 1) % 4
        elif action == 2:
            self.direction = (self.direction - 1) % 4

    def check_apple(self):
        see_apple = False
        if self.direction in [0, 2]: #вверх вниз
            if self.field[self.coords[0], (self.coords[1] - self.direction + 1) % self.field_size] == 1:
                see_apple = True
        else:
            if self.field[(self.coords[0] + 2 - self.direction) % self.field_size, self.coords[1]] == 1:
                see_apple = True
        return see_apple