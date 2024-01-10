from collections import OrderedDict

from day23.puzzle import Blueprint

ROBOT_LIST = [
    "geode",
    "obsidian",
    "clay",
    "ore"
]

OPTIONS = {
    "geode" : True,
    "obsidian" : True,
    "clay" : True,
    "ore" : True,
    "Do nothing" : True
}

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

def max_amt(price_card):
    max_spend = {
        "geode" : 0,
        "obsidian" : 0,
        "clay" : 0,
        "ore" : 0
    }
    for btype in price_card.values():
        for cost in btype:
            max_spend[cost[0]] = max(max_spend[cost[0]], cost[1])
    return max_spend


def dfs(bp, maxspend, time, bots, amt, cache={}):
    if time == 0:
        return amt["geode"]
    
    key = tuple([time, *bots.values(), *amt.values()])
    if key in cache:
        return cache[key]

    maxval = amt["geode"] + bots["geode"] * time

    for bot, recipe in bp.items():
        if bot != "geode" and bots[bot] > maxspend[bot]:
            continue
        wait = 0
        for rtype, ramt in recipe:
            if bots[rtype] == 0:
                break
            wait = max(wait, -(-(ramt - amt[rtype] ) // bots[rtype]))
        else:
            remtime = time - wait - 1
            if remtime <= 0:
                continue
            bots_ = dict(bots)
            amt_ = dict(amt)
            for btype, amount in amt.items():
                amt_[btype] = amount + bots[btype] * (wait + 1)
            for rtype, ramt in recipe:
                amt_[rtype] -= ramt
            bots_[bot] += 1

            for checkbot in ROBOT_LIST:
                if checkbot == "geode":
                    continue
                amt_[checkbot] = min(
                    amt_[checkbot],
                    (maxspend[checkbot] * remtime)
                )

            maxval = max(maxval, dfs(bp, maxspend, remtime, bots_, amt_, cache))

    cache[key] = maxval
    return maxval


def main():
    blueprints = parse_input("input.txt")
    results = {}
    # puzzle 1
    total_time = 24
    for blueprint in blueprints:
        id = int(blueprint.title.split()[-1])
        maxspend = max_amt(blueprint.price_card)
        bots = OrderedDict()
        bots["geode"] = 0
        bots["obsidian"] = 0
        bots["clay"] = 0
        bots["ore"] = 1
        amount = OrderedDict()
        amount["geode"] = 0
        amount["obsidian"] = 0
        amount["clay"] = 0
        amount["ore"] = 0
        max_geode = dfs(
            blueprint.price_card, 
            maxspend, 
            total_time, 
            bots,
            amount,
            dict()
        )
        results[blueprint.title] = id * max_geode

    # answer puzzle 1
    answer_one = sum(results.values())
    print(answer_one)

    # puzzle 2
    total_time = 32
    two_bps = blueprints[:3]
    results = []
    for bp in two_bps:
        maxspend = max_amt(bp.price_card)
        bots = OrderedDict()
        bots["geode"] = 0
        bots["obsidian"] = 0
        bots["clay"] = 0
        bots["ore"] = 1
        amount = OrderedDict()
        amount["geode"] = 0
        amount["obsidian"] = 0
        amount["clay"] = 0
        amount["ore"] = 0
        max_geode = dfs(
            bp.price_card, 
            maxspend, 
            total_time, 
            bots,
            amount,
            {}
        )
        results.append(max_geode)
    
    breakpoint()
    # answer puzzle 2
    answer_two = results[0] * results[1] * results[2]
    print(answer_two)


if __name__ == "__main__":
    main()