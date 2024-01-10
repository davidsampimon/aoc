from collections import namedtuple
from enum import Enum
import sys

sys.setrecursionlimit(1_000_000)
Point = namedtuple("Point", "y x")


def neighbours(pos):
    y, x = pos
    return [
        Point(y, x+1),
        Point(y+1, x),
        Point(y, x-1),
        Point(y-1, x)
    ]


class Entity(Enum):
    ROCK = "#"
    EMPTY_SPACE = "."
    GO_WEST = ">"
    GO_SOUTH = "v"


class Grid():
    def __init__(self, grid, size, start, end):
        self.map = grid
        self.size = size
        self.start = start
        self.end = end
        self.step_map = dict()
        self.puzzle_two = False
        self.cache = dict()

    def draw(self):
        height, width = self.size
        for y in range(height):
            print()
            for x in range(width):
                print(self.map[(y, x)].value, end="")
        print()

    def walk(self, pos=None, count=0, visited=None):
        if visited is None:
            visited = list()
        if pos is None:
            pos = self.start

        if pos in self.cache:
            count += self.cache[pos]["count"]
            visited += self.cache[pos]["segment"]
            pos = self.cache[pos]["exit"]
        
        if pos == self.end:
            return count

        visited.append(pos)

        nbs = neighbours(pos)
        if self.puzzle_two:
            nbs = self.prune_p2(pos, nbs, visited)
        else:
            nbs = self.prune_neighbours(pos, nbs, visited)

        results = [0]
        for nb in nbs:
            results.append(self.walk(nb, count+1, visited.copy()))

        return max(results)

    def within_bounds(self, pos):
        y, x = pos
        return 0 <= y < self.size.y and 0 <= x < self.size.x

    def prune_neighbours(self, pos, nbs, visited):
        result = list()
        for nb in nbs:
            if nb in visited:
                continue
            if not self.within_bounds(nb):
                continue
            match self.map[nb]:
                case Entity.EMPTY_SPACE:
                    result.append(nb)
                case Entity.GO_WEST:
                    if pos.x < nb.x:
                        result.append(nb)
                case Entity.GO_SOUTH:
                    if pos.y < nb.y:
                        result.append(nb)
        return result

    def prune_p2(self, pos, nbs, visited):
        result = list()
        for nb in nbs:
            if nb in self.cache:
                nb = self.cache[nb]["exit"]
            if nb in visited:
                continue
            if not self.within_bounds(nb):
                continue
            match self.map.get(nb):
                case Entity.EMPTY_SPACE:
                    result.append(nb)
                case Entity.GO_WEST:
                    result.append(nb)
                case Entity.GO_SOUTH:
                    result.append(nb)
        return result

    def fill_dead_ends(self):
        empty_spaces = [
            pos for pos, entity in self.map.items()
            if entity is Entity.EMPTY_SPACE
        ]

        while empty_spaces:
            pos = empty_spaces.pop(0)
            nbs = [
                pos for pos in neighbours(pos)
                if self.map.get(pos) is Entity.ROCK
            ]
            if len(nbs) == 3:
                self.map[pos] = Entity.ROCK
                enbs = [
                    pos for pos in neighbours(pos)
                    if self.map.get(pos) is Entity.EMPTY_SPACE
                ]
                for en in enbs:
                    empty_spaces.append(en)

    def fill_hallways(self, pos=None, visited=None):
        if pos is None:
            pos = self.start

        if visited is None:
            visited = [(0, 0)]

        visited.append(pos)
        nbs = neighbours(pos)
        nbs = self.prune_p2(pos, nbs, visited)
        if len(nbs) == 1:
            prev_pos = visited[-2]
            count, exit, sgmmnt = self.segment(pos, visited)
            self.cache[pos] = {"count": count, "exit": exit, "segment": [sgmmnt[0], sgmmnt[-1]]}
            self.cache[sgmmnt[-1]] = {"count": count, "exit": prev_pos, "segment": [sgmmnt[0], sgmmnt[-1]]}
            sgmmnt.pop(0)
            sgmmnt.pop(-1)
            for spos in sgmmnt:
                del self.map[spos]
            self.fill_hallways(pos, visited)
        else:
            for nb in nbs:
                self.fill_hallways(nb, visited)


    def segment(self, pos, visited, count=0, sgmnt=None):
        if sgmnt is None:
            sgmnt = list()
        nbs = neighbours(pos)
        nbs = self.prune_p2(pos, nbs, visited)
        if len(nbs) == 1:
            visited.append(pos)
            sgmnt.append(pos)
            return self.segment(nbs.pop(), visited, count+1, sgmnt)
        else:
            return count, pos, sgmnt



def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    height = len(lines)
    width = len(lines[0])

    grid = dict()
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            grid[Point(y, x)] = Entity(symbol)
            if y == 0 and symbol == ".":
                start = Point(y, x)
            if y == height - 1 and symbol == ".":
                end = Point(y, x)

    return Grid(grid, Point(height, width), start, end)


if __name__ == "__main__":
    grid = data("input.txt")
    print(len(grid.map))

    import time
    # Puzzle 1
    start = time.perf_counter()
    answer = grid.walk()
    print(f"Answer 1: {answer}")
    stop = time.perf_counter()
    print(f"Puzzle 1 takes {stop - start} seconds")

    # Puzzle 2
    rock_list = list()
    for pos, entity in grid.map.items():
        if entity == Entity.ROCK:
            rock_list.append(pos)
    
    for rock in rock_list:
        del grid.map[rock]
    
    print(len(grid.map))
    breakpoint()

    print(len(grid.map))
    start = time.perf_counter()
    grid.fill_hallways()
    stop = time.perf_counter()
    print(f"Fill hallways takes {stop - start} seconds")
    print(len(grid.map))

    start = time.perf_counter()
    grid.puzzle_two = True
    answer = grid.walk()
    print(f"Answer 2: {answer}")
    stop = time.perf_counter()
    print(f"Puzzle 2 takes {stop - start} seconds")
