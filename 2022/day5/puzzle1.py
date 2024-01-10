import re


class CrateStacks():
    def __init__(self, start_state):
        self.state = start_state

    def apply_action(self, step):
        actions = self.parse_instruction(step)
        for _ in range(0, actions[0]):
            crate = self.state[actions[1]].pop()
            self.state[actions[2]].append(crate)

    def apply_action_multiple(self, step):
        actions = self.parse_instruction(step)
        amount = actions[0]
        from_stack = actions[1]
        to_stack = actions[2]
        start_num = len(self.state[from_stack]) - amount
        crates = self.state[from_stack][start_num:]
        self.state[from_stack] = self.state[from_stack][:start_num]
        self.state[to_stack].extend(crates)

    @staticmethod
    def get_starting_state(row_list):
        start_state = {}
        header = row_list[8].split()
        dirty_content = row_list[0:8]

        for stack in header:
            start_state[int(stack)] = []
        
        for row in dirty_content[::-1]:
            for stack in header:
                position = row_list[8].find(stack)
                if not row[position] == " ":
                    start_state[int(stack)].append(row[position])
        return start_state

    @staticmethod
    def parse_instruction(step):
        return list(map(int, re.findall(r'\d+', step)))


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        row_list = f.read().splitlines()

    start_state = CrateStacks.get_starting_state(row_list[0:9])
    crates = CrateStacks(start_state)

    instructions = row_list[10:]
    for step in instructions:
        crates.apply_action(step)

    message = ""
    for key in crates.state.keys():
        message = message + str(crates.state[key][-1])

    print(message)
