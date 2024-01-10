import copy
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __post_init__(self):
        self.sort_index = self.z


@dataclass
class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __hash__(self):
        return hash((self.start, self.end))

    def __post_init__(self):
        self.sort_index = min(self.start, self.end)

    def __repr__(self):
        return f"Brick({self.start}, {self.end})"

    def __copy__(self):
        return copy.deepcopy(self)

    def is_z(self, z):
        return z == min(self.start.z, self.end.z)

    def move_down(self):
        self.start.z -= 1
        self.end.z -= 1

    def collide(self, other):
        x1 = max(
            min(self.start.x, self.end.x),
            min(other.start.x, other.end.x)
        )
        y1 = max(
            min(self.start.y, self.end.y),
            min(other.start.y, other.end.y)
        )
        x2 = min(
            max(self.start.x, self.end.x),
            max(other.start.x, other.end.x)
        )
        y2 = min(
            max(self.start.y, self.end.y),
            max(other.start.y, other.end.y)
        )
        if x1 <= x2 and y1 <= y2:
            return True
        else:
            return False


class Grid:
    def __init__(self, grid):
        self.start_map = grid
        self.total_bricks = len(grid)
        self.max_z = max(
            max(brick.start.z, brick.end.z) for brick in self.start_map
        )
        self.max_x = 0
        self.max_y = 0
        self.view = dict()
        self.support_map = dict()

    def get_by_z(self, z):
        return [
            brick for brick in self.end_map if brick.is_z(z)
        ]

    def get(self, pos):
        return self.view.get(pos)
    
    def move_brick(self, brick, num):
        while True:
            if brick.start.z == 1:
                self.place(brick, num)
                return

            if self.occupied(brick, brick.start.z-1):
                self.place(brick, num)
                return

            brick.move_down()

    def place(self, brick, symbol):
        sx = brick.start.x
        sy = brick.start.y
        sz = brick.start.z
        ex = brick.end.x
        ey = brick.end.y
        ez = brick.end.z


        for z in range(sz, ez + 1):
            for x in range(sx, ex + 1):
                self.max_x = max(x, self.max_x)
                for y in range(sy, ey+1):
                    self.max_y = max(y, self.max_y)
                    self.view[(x, y, z)] = symbol

    def occupied(self, brick, z):
        tmp_brick = copy.copy(brick)
        tmp_brick.move_down()

        sx = tmp_brick.start.x
        sy = tmp_brick.start.y
        ex = tmp_brick.end.x
        ey = tmp_brick.end.y
        z = min(tmp_brick.start.z, tmp_brick.end.z)

        results = set()
        for x in range(sx, ex + 1):
            for y in range(sy, ey + 1):
                if self.get((x, y, z)):
                    results.add(
                        self[(x, y, z)]
                    )

        if len(results) == 0:
            return False
        self.support_map[brick] = results
        return True

    def draw(self):
        for z in range(self.max_z + 1):
            print()
            for x in range(self.max_x + 1):
                symbol = None
                for y in range(self.max_y + 1):
                    symbol = self.view.get((x, y, z), symbol)
                if symbol:
                    print(symbol, end="")
                else:
                    print(".", end="")
        print()

        for z in range(self.max_z + 1):
            print()
            for y in range(self.max_y + 1):
                symbol = None
                for x in range(self.max_x + 1):
                    symbol = self.view.get((x, y, z), symbol)
                if symbol:
                    print(symbol, end="")
                else:
                    print(".", end="")
        print()


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    bricks = list()
    for line in lines:
        start, end = line.split("~")
        sx, sy, sz = [int(i) for i in start.split(",")]
        ex, ey, ez = [int(i) for i in end.split(",")]
        bricks.append(
            Brick(Point(sx, sy, sz), Point(ex, ey, ez))
        )

    bricks.sort
    return bricks

if __name__ == "__main__":
    bricks = data("input.txt")
    grid = Grid(bricks)
    count = 1
    while grid.start_map:
        brick = grid.start_map.pop(0)
        grid.move_brick(brick, count)
        count += 1

    # Puzzle 1
    removals = set()
    for supports in grid.support_map.values():
        if len(supports) == 1:
            removals.update(supports)

    answer = grid.total_bricks - len(removals)
    breakpoint()
    print(f"Answer 1: {answer}")
