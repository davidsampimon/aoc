import time
import copy


class RockGrid:
    def __init__(self, cubes, rounds, size):
        self.cubes = cubes
        self.rounds = rounds
        self.size = size
        self.order = [
            self.tilt_north,
            self.tilt_west,
            self.tilt_south,
            self.tilt_east
        ]
        self.n_cache = dict()
        self.s_cache = dict()
        self.e_cache = dict()
        self.w_cache = dict()

    @property
    def total_load(self):
        total = 0
        for rock in self.rounds:
            total += self.size[0] - rock[0]
        return total
    

    def spin_cycle(self):
        for tilt in self.order:
            tilt()

    def tilt_north(self):
        if str(self.rounds) in self.n_cache:
            return self.n_cache[str(self.rounds)]
        self.rounds = sorted(self.rounds)
        tmp_list = list()
        while self.rounds:
            rock = self.rounds.pop(0)
            rolling = True
            while rolling:
                if rock[0] == 0:
                    tmp_list.append(rock)
                    rolling = False
                else:
                    next_pos = (rock[0] - 1, rock[1])

                    if next_pos in self.cubes or next_pos in tmp_list:
                        tmp_list.append(rock)
                        rolling = False
                    rock = next_pos
        self.n_cache[str(self.rounds)] = tuple(tmp_list)
        self.rounds = self.n_cache[str(self.rounds)]

    def tilt_south(self):
        if str(self.rounds) in self.s_cache:
            return self.s_cache[str(self.rounds)]
        self.rounds = sorted(self.rounds, reverse=True)
        tmp_list = list()
        while self.rounds:
            rock = self.rounds.pop(0)
            rolling = True
            while rolling:
                if rock[0] == self.size[0] - 1:
                    tmp_list.append(rock)
                    rolling = False
                else:
                    next_pos = (rock[0] + 1, rock[1])

                    if next_pos in self.cubes or next_pos in tmp_list:
                        tmp_list.append(rock)
                        rolling = False
                    rock = next_pos

        self.s_cache[str(self.rounds)] = tuple(tmp_list)
        self.rounds = self.s_cache[str(self.rounds)]

    def tilt_east(self):
        if str(self.rounds) in self.e_cache:
            return self.e_cache[str(self.rounds)]

        self.rounds = sorted(self.rounds, key=lambda x: x[1], reverse=True)
        tmp_list = list()
        while self.rounds:
            rock = self.rounds.pop(0)
            rolling = True
            while rolling:
                if rock[1] == self.size[1] - 1:
                    tmp_list.append(rock)
                    rolling = False
                else:
                    next_pos = (rock[0], rock[1] + 1)

                    if next_pos in self.cubes or next_pos in tmp_list:
                        tmp_list.append(rock)
                        rolling = False
                    rock = next_pos
        self.e_cache[str(self.rounds)] = tuple(tmp_list)
        self.rounds = self.e_cache[str(self.rounds)]

    def tilt_west(self):
        if str(self.rounds) in self.w_cache:
            return self.w_cache[str(self.rounds)]
        self.rounds = sorted(self.rounds, key=lambda x: x[1])
        tmp_list = list()
        while self.rounds:
            rock = self.rounds.pop(0)
            rolling = True
            while rolling:
                if rock[1] == 0:
                    tmp_list.append(rock)
                    rolling = False
                else:
                    next_pos = (rock[0], rock[1] - 1)

                    if next_pos in self.cubes or next_pos in tmp_list:
                        tmp_list.append(rock)
                        rolling = False
                    rock = next_pos
        self.w_cache[str(self.rounds)] = tuple(tmp_list)
        self.rounds = self.w_cache[str(self.rounds)]


    def draw(self):
        for y in range(self.size[0]):
            print()
            for x in range(self.size[1]):
                if (y, x) in self.rounds:
                    print("0", end="")
                elif (y, x) in self.cubes:
                    print("#", end="")
                else:
                    print(".", end="")
        print()
  

def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    cubes = list()
    rounds = list()
    height = len(lines)
    width = len(lines[0])
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            match symbol:
                case "#":
                    cubes.append((y, x))
                case "O":
                    rounds.append((y, x))
    
    return RockGrid(cubes, rounds, (height, width))


if __name__ == "__main__":
    grid = data("test.txt")
    
    # puzzle 1
    grid.tilt_north()
    
    answer = 0
    for rock in grid.rounds:
        answer += (grid.size[0] - rock[0])

    print(grid.total_load)
    print(f"Answer 1: {answer}")
