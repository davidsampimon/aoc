"""
Chasing all of the monkeys at once is impossible; you're going to have to focus on the two most active monkeys if you want any hope of getting your stuff back. Count the total number of times each monkey inspects items over 20 rounds

The level of monkey business in this situation can be found by multiplying these together

Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. What is the level of monkey business after 20 rounds of stuff-slinging simian shenanigans
"""

import heapq
import operator
from collections import deque


class Item:
    def __init__(self, name, worry_level):
        self.name = name
        self.worry_level = worry_level
    
    def __repr__(self):
        return f"Name: {self.name}, worried: {self.worry_level}"

class Monkey:
    def __init__(self, name, operation, test, test_true, test_false):
        self.name = name
        self.num = operation.split()[-1]
        self.mod = operation.split()[-2]
        self.test_num = int(test.split()[-1])
        self.test_true = int(test_true.split()[-1])
        self.test_false = int(test_false.split()[-1])
        self.ops = { "+": operator.add, "-": operator.sub, "*": operator.mul}
        self.items = deque()
        self.items_inspected = 0

    def __repr__(self):
        return f"Name: {self.name} \n" \
            f"Items: {self.items} \n" \
            f"Operation: {self.mod} {self.num} \n" \
            f"Test: {self.test_num}, true: {self.test_true}, false: {self.test_false} \n" 

    def operation(self, item):
        if self.num == "old":
            return self.ops[self.mod](item.worry_level, item.worry_level)
        return self.ops[self.mod](item.worry_level, int(self.num))

    def test(self, item):
        return item.worry_level % self.test_num == 0

    def turn(self, monkey_list, broken=False):
        for _ in range(0, len(self.items)):
            item = self.items.popleft()
            item.worry_level = self.operation(item)
            if broken:
                item.worry_level = item.worry_level % 9699690
            else:
                item.worry_level = item.worry_level // 3
            if self.test(item):
                monkey_list[self.test_true].items.append(item)
            else:
                monkey_list[self.test_false].items.append(item)
            self.items_inspected += 1
        return monkey_list


def parse_input(puzzle_input):
    item_index = 0
    monkeys = []
    with open(puzzle_input, "r") as f:
        for row in f:
            if "Monkey" in row:
                name = row.strip(":\n")
                index = int(''.join(filter(str.isdigit, name)))
            if "Starting" in row:
                worry_level_list = row.strip().replace(
                    "Starting items: ",
                    ""
                ).split(", ")
            if "Operation" in row:
                operation = row.strip()
            if "Test" in row:
                test = row.strip()
            if "true" in row:
                test_true = row.strip()
            if "false" in row:
                test_false = row.strip()
                monkeys.append(
                    Monkey(
                        name,
                        operation,
                        test,
                        test_true,
                        test_false
                    )
                )
                for worry_level in worry_level_list:
                    item = Item(item_index, int(worry_level))
                    monkeys[index].items.append(item)
                    item_index += 1
    return monkeys


if __name__ == "__main__":
    monkeys = parse_input("input.txt")
    rounds = 10000

    for round in range(0, rounds):
        for monkey in monkeys:
            monkey = monkey.turn(monkeys, broken=True)
    
    result = []
    for monkey in monkeys:
        result.append(monkey.items_inspected)

    top_2 = heapq.nlargest(2, result)
    monkey_business = top_2[0] * top_2[1]
    print(monkey_business)
