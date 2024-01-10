from collections import namedtuple
import heapq


Point = namedtuple("Point", "z y x")


def look_down(point):
    z, y, x = point
    return Point(z-1, y, x)


class Brick:
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end
        self.supports_below = set()
        self.supports_top = set()
        self.is_supported = True

    @property
    def grid(self):
        points = list()
        for z in range(self.start.z, self.end.z + 1):
            for y in range(self.start.y, self.end.y + 1):
                for x in range(self.start.x, self.end.x + 1):
                    points.append(
                        Point(z, y, x)
                    )
        return points

    def __repr__(self):
        return f"B({self.start}, {self.end})"

    def __lt__(self, other):
        return self.start < other.start

    def copy(self):
        return Brick(self.id, self.start, self.end)

    def move_down(self):
        sz, sy, sx = self.start
        ez, ey, ex = self.end
        self.start = Point(sz-1, sy, sx)
        self.end = Point(ez-1, ey, ex)


class Grid:
    def __init__(self, bricks):
        self.start = bricks
        self.end = dict()
        self.queue = bricks.copy()
        self.collission_map = dict()
        self.move_all_down()
        self.fall_queue = list()

    def place(self, brick):
        self.end[brick.id] = brick
        for pos in brick.grid:
            self.collission_map[pos] = brick.id

    def move_brick_down(self, brick):
        while True:
            if brick.start.z == 1 or brick.end.z == 1:
                self.place(brick)
                return
            cast_ahead = brick.copy()
            cast_ahead.move_down()
            collissions = [
                self.collission_map[pos] for pos in cast_ahead.grid
                if pos in self.collission_map
            ]
            if collissions:
                for sb in collissions:
                    brick.supports_below.add(sb)
                    self.end[sb].supports_top.add(brick.id)
                self.place(brick)
                return
            brick.move_down()

    def move_all_down(self):
        while self.queue:
            brick = self.queue.pop(0)
            self.move_brick_down(brick)

    def check_falling(self):
        while self.fall_queue:
            brick = heapq.heappop(self.fall_queue)

            support = any(
                self.end[sb].is_supported for sb in brick.supports_below
            )

            if not support:
                brick.is_supported = False

            if not brick.is_supported:
                for id in brick.supports_top:
                    tb = self.end[id]
                    heapq.heappush(self.fall_queue, tb)

        count = 0
        for brick in self.end.values():
            if not brick.is_supported:
                count += 1

        return count - 1

    def reset(self):
        for brick in self.end.values():
            brick.is_supported = True


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    bricks = list()
    for index, line in enumerate(lines):
        start, end = line.split("~")
        sx, sy, sz = [int(i) for i in start.split(",")]
        ex, ey, ez = [int(i) for i in end.split(",")]
        bricks.append(
            Brick(index + 1, Point(sz, sy, sx), Point(ez, ey, ex))
        )

    return sorted(bricks, key=lambda x: x.start.z)


if __name__ == "__main__":
    bricks = data("input.txt")
    assert bricks[0].start.z == 1

    brick = Brick(9, Point(1, 1, 1), Point(3, 3, 3))
    assert Point(2, 2, 2) in brick.grid

    grid = Grid(bricks)
    grid.move_all_down()

    # Puzzle 1
    support_map = dict()
    for brick in bricks:
        support_map[brick.id] = set()

    for point, id in grid.collission_map.items():
        hit = grid.collission_map.get(look_down(point))
        if hit and hit != id:
            support_map[id].add(hit)

    singles = set()
    for supports in support_map.values():
        if len(supports) == 1:
            singles.update(supports)

    answer = len(bricks) - len(singles)
    print(f"Answer 1: {answer}")

    # puzzle 2
    answer = 0
    for id in singles:
        grid.end[id].is_supported = False
        heapq.heappush(grid.fall_queue, grid.end[id])
        answer += grid.check_falling()
        grid.reset()

    print(f"Answer 2: {answer}")
