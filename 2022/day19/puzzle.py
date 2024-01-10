import heapq
from copy import deepcopy

TOTAL_MINUTES = 24

ROBOT_LIST = [
    "geode",
    "obsidian",
    "clay",
    "ore"
]

class Inventory:
    def __init__(self):
        self.robots = []
        self.materials = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0,
        }

    def prio_score(self, minute):
        score = 0
        stock = self._project_production(self.materials, minute)
        score += stock["geode"] * 1000
        score += stock["obsidian"] * 100
        score += stock["clay"] * 10
        score += stock["ore"]
        return score
    
    def _project_production(self, materials, minute):
        stock = deepcopy(materials)
        for bot in self.robots:
            stock[bot] += minute
        return stock

    def add_material(self, material):
        self.materials[material] += 1

    def remove_material(self, material, amount):
        self.materials[material] -= amount

    def add_robot(self, robot):
        self.robots.append(robot)

    def play_round(self):
        for robot in self.robots:
            self.add_material(robot)

    def __repr__(self):
        return f"{self.robots}, {self.materials}"

class Game:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.price_card = blueprint.price_card
        # self.max_robots = self._max_robots()
        # self.max_materials = {"ore01": 0}
        # self._init_max_materials()
        self.path_counter = 1
        self.top_prio = [0 for _ in range(100000)]

    # def _init_max_materials(self):
    #     for bot in ROBOT_LIST:
    #         for minute in range(TOTAL_MINUTES + 1):
    #             self.max_materials[bot + str(minute)] = 0

    # def _max_robots(self):
    #     max_robot = {key: 0 for key in ROBOT_LIST}
    #     for item in self.price_card.values():
    #         for cost in item:
    #             max_robot[cost[0]] = max(max_robot[cost[0]], cost[1])
    #     return max_robot

    def update_max_materials(self, minute, material, found_value):
        if minute < 0:
            return

        if found_value > self.max_materials[material + str(minute)]:
            self.max_materials[material + str(minute)] = found_value
            return self.update_max_materials(minute-1, material, found_value+1)


    # def is_dead_end(self, inventory, time_remaining):
    #     max_geode = self.max_materials["geode" + str(time_remaining)]
        
    #     if inventory.materials["geode"] < max_geode - 1:
    #         return True
        
    #     return False

    def clean_results(self, results, inventory, time_remaining):
        # if possible to build a geode bot, build only that
        if "geode" in results:
            return ["geode"]

        # consider how much of every type can be build by the factory in the 
        # remaining time. If we got more of that, do not produce more of that 
        # robot
        for robot_func in results:
            if robot_func == "Do nothing":
                continue
            costs = self.price_card[robot_func]
            if all([(inventory.materials[cost[0]] * time_remaining) > cost[1]
                for cost in costs]):
                    results.remove(robot_func)
        return results


    def play_round(self, inventory, time_remaining):
        if time_remaining == 0:
            return inventory.materials["geode"]

        # if self.is_dead_end(inventory, time_remaining):
        #     return inventory.materials["geode"]
        
        dirty_options = self.options(inventory)

        if dirty_options == "Do nothing":
            inventory.play_round()
            return self.play_round(inventory, time_remaining-1)

        options = self.clean_results(dirty_options, inventory, time_remaining)

        geode_results = []
        for robot_func in options:
            new_inventory = deepcopy(inventory)

            if robot_func == "Do nothing":
                new_inventory = self.produce_gains(time_remaining, new_inventory)
                geode_results.append(
                    self.play_round(new_inventory, time_remaining-1)
                )
            else:
                self.path_counter += 1
                new_inventory = self.pay_robot(new_inventory, robot_func)
                new_inventory = self.produce_gains(time_remaining, new_inventory)
                new_inventory.add_robot(robot_func)
                geode_results.append(
                    self.play_round(new_inventory, time_remaining-1)
                )
        return max(geode_results)

    def produce_gains(self, minute, inventory):
        inventory.play_round()
        # for material in ROBOT_LIST:
        #     self.update_max_materials(
        #         minute,
        #         material,
        #         inventory.materials[material]
        #     )
        return inventory

    def pay_robot(self, inventory, robot):
        for cost in self.blueprint.price_card[robot]:
            inventory.remove_material(cost[0], cost[1])
        return inventory

    def options(self, inventory):
        result = []
        bot_list = ROBOT_LIST

        # for bot in bot_list:
        #     amount = inventory.robots.count(bot)
        #     if amount > self.max_robots[bot]:
        #         bot_list.remove(bot)

        materials = inventory.materials
        for robot in bot_list:
            if all(
                [cost[1] <= materials[cost[0]] for cost in self.price_card[robot]]):
                result.append(robot)
        if len(result) == 0:
            return "Do nothing"
        result.append("Do nothing")
        return result



class Blueprint:
    def __init__(self, title):
        self.title = title
        self.price_card = {}

    def add_price_item(self, robot_func, cost):
        self.price_card[robot_func] = cost

    def __repr__(self):
        return f"{self.title}: {self.price_card}"

def parse_input(data):
    with open(data, "r") as f:
        data_list = f.read().splitlines()
    blueprint_list = []
    for row in data_list:
        blueprint_list.append(parse_line(row))
    return blueprint_list
        
def parse_line(row_data):
    parts = row_data.split(":")
    blueprint = Blueprint(parts[0])
    robot_strings = parts[1].split(".")
    for robot_string in robot_strings:
        if len(robot_string) < 3:
            continue
        string_parts = robot_string.split()
        robot_func = string_parts[1]
        cost = [(string_parts[5], int(string_parts[4]))]
        if len(string_parts) > 6:
            cost.append((string_parts[8], int(string_parts[7])))
        blueprint.add_price_item(robot_func, cost)
    return blueprint


def play_scenario(blueprint):
    time_remaining = TOTAL_MINUTES
    game = Game(blueprint)
    inventory = Inventory()
    inventory.add_robot("ore")
    max_geode = game.play_round(inventory, time_remaining)
    breakpoint()
    blueprint_num = int(blueprint.title.split()[-1])
    return blueprint_num * max_geode
    
def main():
    blueprints = parse_input("test.txt")
    results = {}
    for blueprint in blueprints:
        results[blueprint] = play_scenario(blueprint)
        print(str(blueprint.title) + ": " + str(results))
        breakpoint()
    # answer puzzle 1
    answer_one = sum(results.values())
    print(answer_one)

    

if __name__ == "__main__":
    main()