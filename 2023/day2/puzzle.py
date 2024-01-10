from functools import reduce
import re

MAX_COLORS = {"red": 12, "green": 13, "blue": 14 }


def parse_round(dirty_round):
    cubes_dict = {}
    cubes = dirty_round.split(",")
    for cube in cubes:
        amount = re.findall(r'\d+', cube)
        for colour in MAX_COLORS.keys():
            if colour in cube:
                cubes_dict[colour] = int(amount[0])
    return cubes_dict


def parse_line(row):
    split_list = row.split(":")
    game = split_list.pop(0)
    id = re.findall(r'\d+', game)[0]
    dirty_rounds = split_list[0].split(";")
    rounds = []
    for round in dirty_rounds:
        rounds.append(parse_round(round))
    return id, rounds


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

results = {}
for row in lines:
    id, rounds = parse_line(row)
    results[id] = rounds



# Puzzle 1
answer = 0
for id, rounds in results.items():
    for round in rounds:
        for colour, amount in round.items():
            if amount > MAX_COLORS[colour]:
                id = 0
    answer += int(id)

print(f"Answer 1: {answer}")


# Puzzle 2
answer = 0
power = []
for id, rounds in results.items():
    cube_dict = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    for round in rounds:
        for colour, amount in round.items():
            cube_dict[colour] = max(cube_dict[colour], amount)

    power.append(reduce((lambda x, y: x * y), cube_dict.values()))

print(f"Answer 2: {sum(power)}")
