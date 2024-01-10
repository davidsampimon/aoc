from enum import Enum

NUMBER_OF_CYCLES = 1_000_000_000


def rotate_clockwise(platform):
    # (0, 0) => (max_y, 0)
    # (0, 1) => (max_y - 1, 0)
    # (1, 0) => (max_y, 1)
    # (1, 1) => (max_y - 1, 1)
    max_y = max(y for y, x in platform)
    rotated_platform = {
        (x, max_y - y): platform[(y, x)]
        for y, x in platform
    }
    return rotated_platform


def cycle_spin(platform):
    for _ in range(4):
        platform = tilt_north(platform)
        platform = rotate_clockwise(platform)
    return platform


def tilt_north(platform):
    max_x = max(x for y, x in platform)

    for x in range(max_x+1):
        tilt_column_north(x, platform)
    return platform


def tilt_column_north(x, platform):
    max_y = max(y for y, x in platform)
    next_empty_y = 0
    for current_y in range(max_y+1):
        object_at_pos = platform[(current_y, x)]

        if object_at_pos == Entity.SQUARE_ROCK:
            next_empty_y = current_y + 1
            continue

        if object_at_pos == Entity.ROUND_ROCK:
            platform[(current_y, x)] = Entity.EMPTY
            platform[(next_empty_y, x)] = Entity.ROUND_ROCK
            next_empty_y += 1
            continue


def total_load(platform):
    total = 0
    max_y = max(y for y, x in platform)
    for pos, object in platform.items():
        if object == Entity.ROUND_ROCK:
            total += (max_y + 1) - pos[0]
    return total


class Entity(Enum):
    EMPTY = "."
    ROUND_ROCK = "O"
    SQUARE_ROCK = "#"


def data(filepath):
    platform = dict()

    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            object_at_pos = Entity(symbol)
            platform[(y, x)] = object_at_pos

    return platform


def draw(platform):
    max_y = max(y for y, x in platform)
    max_x = max(x for y, x in platform)

    for y in range(max_y+1):
        print()
        for x in range(max_x+1):
            print(platform[(y, x)].value, end="")


if __name__ == "__main__":
    platform = data("input.txt")

    # Puzzle 1:
    platform = tilt_north(platform)
    answer = total_load(platform)
    print(f"Answer 1: {answer}")

    # Puzzle 2
    p_two = data("input.txt")
    previous_states = {}

    iteration = 0
    while iteration < NUMBER_OF_CYCLES:
        p_two = cycle_spin(p_two)
        key = frozenset(p_two.items())

        if key in previous_states:
            prev_iter = previous_states[key]
            cycle_length = iteration - prev_iter
            print(f"Cycle found in iteration {iteration}, length: {cycle_length}")

            iterations_left = NUMBER_OF_CYCLES - iteration
            cycles = iterations_left % cycle_length
            iteration = NUMBER_OF_CYCLES - cycles  # fast forward to end
            previous_states = {}

        previous_states[key] = iteration
        iteration += 1

    answer = total_load(p_two)
    print(f"Answer 2: {answer}")
