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

class entity(Enum):
    EMPTY_SPACE = "."

    def __repr__(self):
        return str(self.value)


class Grid:
    def __init__(self, grid, size, start):
        self.map = grid
        self.size = size
        self.start = start
    
    def draw(self):
        height, width = self.size
        for y in range(height):
            print()
            for x in range(width):
                if (y, x) in self.map:
                    print(self.map[Point(y, x)].value, end="")
                else:
                    print(" ", end="")
        print()

def find_segments(grid, pos, visited=None, segments=None):
    if segments is None:
        segments = dict()

    if visited is None:
        visited = [(-1, 1)]

    nbs = [
        nb for nb in neighbours(pos) if nb in grid and nb not in visited
    ]

    if len(nbs) == 1:
        prev_pos = visited[-1]
        visited.append(pos)

        count, exit, sgmmnt = walk_segment(pos, prev_pos)
        segments[pos] = {"count": count, "exit": exit, "pair": sgmmnt[-1] }
        segments[sgmmnt[-1]] = {"count": count, "exit": prev_pos, "pair": pos}
        sgmmnt.pop(0)
        sgmmnt.pop(-1)
        for spos in sgmmnt:
            del grid[spos]
        find_segments(grid, pos, visited, segments)
    else:
        for nb in nbs:
            find_segments(grid, nb, visited, segments)

    return grid, segments


def walk_segment(pos, prev_pos, segment=None, count=0):
    if segment is None:
        segment = list()

    nbs = [
        nb for nb in neighbours(pos)
        if nb in grid and
        nb not in segment and
        nb != prev_pos
    ]

    if len(nbs) == 1:
        segment.append(pos)
        return walk_segment(nbs[0], pos, segment, count+1)
    else:
        return count, pos, segment


def walk(grid, pos, end, segments, count=0, visited=None):
    if pos == end:
        return count
    
    if visited is None:
        visited = list()
    
    visited.append(pos)
    if pos in segments:
        visited.append(segments[pos]["pair"])
        count += segments[pos]["count"]
        pos = segments[pos]["exit"]

    nbs = [nb for nb in neighbours(pos) if nb in grid and nb not in visited]
    del grid[pos]


    result = [0]
    if nbs:
        for nb in nbs:
            result.append(
                walk(grid.copy(), nb, end, segments, count+1, visited.copy())
            )

    return max(result)


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    height = len(lines)

    grid = dict()
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol in ".>v":
                grid[Point(y, x)] = entity.EMPTY_SPACE
            if y == 0 and symbol == ".":
                start = Point(y, x)
            if y == height - 1 and symbol == ".":
                end = Point(y, x)

    return grid, start, end


if __name__ == "__main__":
    grid, start, end = data("input.txt")
    print(len(grid))
    grid, segments = find_segments(grid, start)
    print(len(grid))

    import time
    # Puzzle 2
    begin = time.perf_counter()
    answer = walk(grid, start, end, segments)
    print(answer)
    stop = time.perf_counter()
    print(f"Puzzle 2 in {stop - begin} seconds")
