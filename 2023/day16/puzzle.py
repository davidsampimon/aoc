from enum import Enum
import time


class Entity(Enum):
    EMPTY_SPACE = "."
    BACK_MIRROR = "\\"
    FRONT_MIRROR = "/"
    HOR_SPLITTER = "-"
    VER_SPLITTER = "|"


class Grid:
    def __init__(self, grid, size):
        self.map = grid
        self.size = size
        self.beams = list()
        self.history = set()
        self.tiles = set()

    @property
    def energized(self):
        return len(self.tiles)

    def set_beam(self, beam):
        self.beams.append(beam)

    def draw(self):
        height, width = self.size

        for y in range(height):
            print()
            for x in range(width):
                obj = "#" if (y, x) in self.tiles else self.get((y, x)).value
                print(obj, end="")
        print()

    def get(self, pos):
        return self.map.get(pos)

    def add_to_history(self, beam):
        if self.get(beam.pos):
            self.history.add((beam.pos, beam.direction))
            self.tiles.add(beam.pos)

    def turn(self):
        beams = list()
        while self.beams:
            beam = self.beams.pop()
            if (beam.pos, beam.direction) in self.history:
                continue
            self.add_to_history(beam)
            entity = self.get(beam.pos)
            if entity:
                beams += self.next_beams(beam, entity)
        self.beams = beams

    def move(self):
        for beam in self.beams:
            beam.next_pos()

    def next_beams(self, beam, entity):
        beams = list()
        match entity:
            case Entity.BACK_MIRROR:
                if beam.direction in (1, 3):
                    beam.rotate("clockwise")
                elif beam.direction in (2, 0):
                    beam.rotate("counter-clockwise")
                beams.append(beam)
            case Entity.FRONT_MIRROR:
                if beam.direction in (1, 3):
                    beam.rotate("counter-clockwise")
                elif beam.direction in (2, 0):
                    beam.rotate("clockwise")
                beams.append(beam)
            case Entity.HOR_SPLITTER:
                if beam.direction in (1, 3):
                    beams.append(beam)
                elif beam.direction in (0, 2):
                    beams.append(Beam(beam.pos, 1))
                    beams.append(Beam(beam.pos, 3))
            case Entity.VER_SPLITTER:
                if beam.direction in (0, 2):
                    beams.append(beam)
                elif beam.direction in (1, 3):
                    beams.append(Beam(beam.pos, 0))
                    beams.append(Beam(beam.pos, 2))
            case _:
                beams.append(beam)
        return beams


class Beam:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def __eq__(self, other):
        if isinstance(other, Beam):
            return (
                (self.pos == other.pos) and (self.direction == other.direction)
            )

    def __hash__(self):
        return hash((self.pos, self.direction))

    def __repr__(self):
        return f"{self.pos}: {self.direction}"

    def next_pos(self):
        match self.direction:
            case 1:
                self.pos = (self.pos[0], self.pos[1] + 1)
            case 2:
                self.pos = (self.pos[0] + 1, self.pos[1])
            case 3:
                self.pos = (self.pos[0], self.pos[1] - 1)
            case 0:
                self.pos = (self.pos[0] - 1, self.pos[1])

    def rotate(self, direction):
        match direction:
            case "clockwise":
                self.direction = (self.direction + 1) % 4
            case "counter-clockwise":
                self.direction = (self.direction - 1) % 4


def data(filepath):
    grid = dict()
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    height = len(lines)
    width = len(lines[0])

    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            grid[(y, x)] = Entity(symbol)

    return Grid(grid, (height, width))


if __name__ == "__main__":
    grid = data("input.txt")
    grid.set_beam(Beam((0, 0), 1))

    while grid.beams:
        grid.turn()
        grid.move()

    print(f"Answer 1: {grid.energized}")

    # Puzzle 2
    grids = list()
    height = grid.size[0]
    width = grid.size[1]
    for y in range(height):
        y_begin = Grid(grid.map, grid.size)
        y_begin.set_beam(Beam((y, 0), 1))
        grids.append(y_begin)
        y_end = Grid(grid.map, grid.size)
        y_end.set_beam(Beam((y, width - 1), 3))
        grids.append(y_end)

    for x in range(width):
        x_top = Grid(grid.map, grid.size)
        x_top.set_beam(Beam((0, x), 2))
        grids.append(x_top)
        x_bottom = Grid(grid.map, grid.size)
        x_bottom.set_beam(Beam((height - 1, x), 0))
        grids.append(x_bottom)

    answer = 0
    start = time.perf_counter()
    count = 0
    while grids:
        grid = grids.pop(0)
        if grid.beams:
            grid.turn()
            grid.move()
            answer = max(answer, grid.energized)
            grids.append(grid)
            count += 1
    stop = time.perf_counter()
    print(f"Answer 2: {answer}")
    print(f"In {stop - start} seconds!")
