from itertools import product
import re


def springs_to_config(spring_data):
    matches = re.findall(r"#+", spring_data)
    return [len(spring) for spring in matches]


def all_combinations(spring):
    seq = spring["data"]
    indices = spring["wildcards"]
    symbols = "#."
    count = 0
    for symbol in product(symbols, repeat=len(indices)):
        for index, char in zip(indices, symbol):
            seq[index] = char

        seq_str = ''.join(seq)
        if springs_to_config(seq_str) == spring["config"]:
            count += 1

    return count

class P2Solver():
    def __init__(self, spring):
        self.data = spring["data"]
        self.config = spring["config"]
        self.length = len(self.data)

    def dp_all_combinations(self, spring, memo=dict()):

        i = spring["data"].index("?")
        str_part = spring["data"][:i]

        part_a = str_part + "#"
        part_b = str_part + "."

        config = springs_to_config(part_a)
        for index, group in enumerate(config):
            if group != self.config[index]:
                return
        
    





    breakpoint()



    key = str(spring["config"]) + str(spring["data"])
    if key in memo:
        return memo[key]


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    data_list = list()
    for line in lines:
        dir_data = line.split()
        data_list.append({
            "data": list(dir_data[0]),
            "config": [int(x) for x in dir_data[1].split(",")],
            "wildcards": [
                pos for pos, char in enumerate(dir_data[0]) if char == "?"
            ],
        })

    return data_list


if __name__ == "__main__":
    springs = data("test.txt")

    # Puzzle 1
    # count = 0
    # for spring in springs:
    #     options = all_combinations(spring)
    #     for option in options:
    #         if springs_to_config(option) == spring["config"]:
    #             count += 1

    # print(f"Answer 1: {count}")

    # Puzzle 2
    springs_two = list()
    for spring in springs:
        data_list = ["".join(spring["data"])] * 5
        spring_two = {
            "data": "?".join(data_list),
            "config": spring["config"] * 5
        }
        springs_two.append(spring_two)

    breakpoint()
    spring = {"data": "#.#.##?##?...?..#"}
    dp_all_combinations(spring)

    answer = 0
    length = len(springs)
    for index, spring in enumerate(springs):
        breakpoint()
        spring["data"].insert(0, "?")
        subtotal = all_combinations(spring) * 4
        del spring["data"][-1]
        answer += all_combinations(spring) * subtotal

    print(f"Answer 2: {answer}")
