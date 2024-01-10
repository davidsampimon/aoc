import re


def get_perimeter(coord):
    y = coord[0]
    x_span = coord[1]
    num_coords = [(y, x) for x in range(x_span[0], x_span[1])]
    x_min = min(x_span) - 1
    x_max = max(x_span) + 1

    perimeter = list()

    for y in range(y-1, y+2):
        perimeter += [
            (y, x) for x in range(x_min, x_max) if (y, x) not in num_coords
        ]
    return perimeter


def data(input_file):
    with open(input_file, "r") as f:
        lines = f.read().splitlines()

    num_grid = {}
    collission_map = {}
    symbol_grid = {}
    for y, line in enumerate(lines):
        for match in re.finditer(r"\d+", line):
            span = match.span()
            num_grid[(y, span)] = int(match.group())
            for x in range(span[0], span[1]):
                collission_map[(y, x)] = (y, span)

        for x, char in enumerate(line):
            if char != "." and not char.isdigit():
                symbol_grid[(y, x)] = char

    return num_grid, symbol_grid, collission_map


if __name__ == "__main__":
    nums, symbols, collission_map = data("input.txt")

    # puzzle 1
    answer = 0
    for coords, value in nums.items():
        perimeter = get_perimeter(coords)

        if any([coord in symbols for coord in perimeter]):
            answer += value
    print(f"Answer 1: {answer}")

    # puzzle 2
    gear_coords = []
    for coord, symbol in symbols.items():
        if symbol == "*":
            gear_coords.append(coord)

    answer = 0
    for gear in gear_coords:
        perimeter = get_perimeter((gear[0], (gear[1], gear[1]+1)))
        parts_set = set()

        for coord in perimeter:
            if coord in collission_map:
                part = nums[collission_map[coord]]
                parts_set.add(part)

        if len(parts_set) == 2:
            gear_ratio = parts_set.pop() * parts_set.pop()
            answer += gear_ratio

    print(f"Answer 2: {answer}")
