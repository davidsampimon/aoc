from day10.puzzle1 import CrateStacks

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        row_list = f.read().splitlines()

    start_state = CrateStacks.get_starting_state(row_list[0:9])
    crates = CrateStacks(start_state)

    instructions = row_list[10:]
    for step in instructions:
        crates.apply_action_multiple(step)

    message = ""
    for key in crates.state.keys():
        message = message + str(crates.state[key][-1])

    print(message)