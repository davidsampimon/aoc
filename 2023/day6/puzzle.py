from functools import reduce


def data_one(filepath):
    with open(filepath, "r") as f:
        dir_data = list()
        for row in f:
            dir_data.append(row.split())

    data = list(zip(dir_data[0], dir_data[1]))

    data.pop(0)

    return [(int(x[0]), int(x[1])) for x in data]


def data_two(filepath):
    with open(filepath, "r") as f:
        dir_data = list()
        for row in f:
            dir_data.append(row.split())

    for dd in dir_data:
        del dd[0]

    data = list()
    for dd in dir_data:
        num_string = ""
        for num in dd:
            num_string += num
        data.append(num_string)

    return [int(x) for x in data]


def sim_game(wait, game):
    speed = wait
    time = game[0] - wait
    return time * speed


def play_game(game):
    time_limit = game[0]
    record = game[1]
    count = 0

    for wait in range(0, time_limit):
        outcome = sim_game(wait, game)
        if outcome > record:
            count += 1
    return count


if __name__ == "__main__":
    games = data_one("input.txt")
    results = list()

    for game in games:
        results.append(play_game(game))

    answer = reduce((lambda x, y: x * y), results)
    print(f"Answer 1: {answer}")

    # puzzle 2
    game = data_two("input.txt")
    results = list()
    results = play_game(game)

    answer = results
    print(f"Answer 2: {answer}")
