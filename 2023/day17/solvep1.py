from enum import Enum
import heapq


class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP = (-1, 0)


def next_directions(direction):
    match direction:
        case Direction.RIGHT:
            return [Direction.RIGHT, Direction.DOWN, Direction.UP]
        case Direction.DOWN:
            return [Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        case Direction.LEFT:
            return [Direction.LEFT, Direction.DOWN, Direction.UP]
        case Direction.UP:
            return [Direction.UP, Direction.LEFT, Direction.RIGHT]


def add(pos, pos_other):
    return (pos[0] + pos_other[0], pos[1] + pos_other[1])


class State:
    def __init__(self, loss, pos, direction, count):
        self.loss = loss
        self.pos = pos
        self.direction = direction
        self.count = count
        self.key = (pos, direction, count)

    def __lt__(self, other):
        return (self.loss) < (other.loss)


def solve(grid, end):
    seen = set()
    Queue = [
        State(0, (0, 0), Direction.RIGHT, 0),
        State(0, (0, 0), Direction.DOWN, 0)
    ]

    while Queue:
        s = heapq.heappop(Queue)
        if s.key in seen:
            continue
        seen.add(s.key)

        loss, pos, direction, count = s.loss, s.pos, s.direction, s.count

        if pos == end:
            return loss

        directions = next_directions(direction)
        new_pos = add(pos, directions[0].value)
        if count < 3 and new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[0], count+1)
            )

        new_pos = add(pos, directions[1].value)
        if new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[1], 1)
            )

        new_pos = add(pos, directions[2].value)
        if new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[2], 1)
            )


def solve_p2(grid, end):
    seen = set()
    Queue = [
        State(0, (0, 0), Direction.RIGHT, 0),
        State(0, (0, 0), Direction.DOWN, 0)
    ]

    while Queue:
        s = heapq.heappop(Queue)
        if s.key in seen:
            continue
        seen.add(s.key)

        loss, pos, direction, count = s.loss, s.pos, s.direction, s.count

        if pos == end and count >= 4:
            return loss

        directions = next_directions(direction)
        new_pos = add(pos, directions[0].value)
        if count < 10 and new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[0], count+1)
            )

        new_pos = add(pos, directions[1].value)
        if count > 3 and new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[1], 1)
            )

        new_pos = add(pos, directions[2].value)
        if count > 3 and new_pos in grid:
            heat_loss = loss + grid[new_pos]
            heapq.heappush(
                Queue, State(heat_loss, new_pos, directions[2], 1)
            )


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        grid = dict()
        height = len(lines)
        width = len(lines[0])

        for y, line in enumerate(lines):
            for x, heat_loss in enumerate(line):
                grid[(y, x)] = int(heat_loss)

        return grid, (height-1, width-1)


if __name__ == "__main__":
    grid, end = data("input.txt")

    # Puzzle 1
    answer = solve(grid, end)
    print(f"Answer 1: {answer}")

    # Puzzle 2
    answer = solve_p2(grid, end)
    print(f"Answer 2: {answer}")
