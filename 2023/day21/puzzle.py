import sys
from enum import Enum
sys.setrecursionlimit(1_000_000_000)


def neighbours(pos):
    y, x = pos
    return [
        (y, x+1),
        (y+1, x),
        (y, x-1),
        (y-1, x)
    ]


class Entity(Enum):
    ROCK = "#"
    EMPTY_SPACE = "."
    START = "S"



class Grid:
    def __init__(self, grid, size, start):
        self.map = grid
        self.size = size
        self.start = start
        self.step_map = dict()

    def get(self, pos):
        height, width = self.size

        return self.map[
            (pos[0] % height, pos[1] % width)
        ]

    def rel_pos(self, pos):
        height, width = self.size

        return (pos[0] % height, pos[1] % width)

    def draw(self):
        height, width = self.size

        for y in range(height):
            print()
            for x in range(width):
                print(self.map[(y, x)].value, end="")
        print()

    def fill_step_map(self, steps):
        if steps in self.step_map:
            return self.step_map[steps]

        if steps == 0:
            self.step_map[steps] = {(self.start)}
            return self.step_map[steps]

        if steps == 1:
            self.step_map[steps] = set(self._valid_neighbours(self.start))
            return self.step_map[steps]

        if steps > 2:
            active_tiles = self.fill_step_map(steps-1) - self.fill_step_map(steps-3)
        else:
            active_tiles = self.fill_step_map(steps-1)

        results = list()
        for tile in active_tiles:
            results += self._valid_neighbours(tile)
        self.step_map[steps] = self.fill_step_map(steps-2).copy()
        for pos in results:
            self.step_map[steps].add(pos)

        return self.step_map[steps]

    def _valid_neighbours(self, tile):
        return [nb for nb in neighbours(tile) if self.get(nb) is not Entity.ROCK]


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    height = len(lines)
    width = len(lines[0])

    grid = dict()
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            grid[(y, x)] = Entity(symbol)
            if symbol == "S":
                start_pos = (y, x)

    return Grid(grid, (height, width), start_pos)


if __name__ == "__main__":
    grid = data("input.txt")

    # Puzzle 1
    steps = 64
    grid.fill_step_map(steps)
    answer = len(grid.step_map[steps])
    print(f"Answer 1: {answer}")

