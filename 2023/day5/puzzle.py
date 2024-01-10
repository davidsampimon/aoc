import re


LOOKUP_ORDER = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]

def flatten(l):
    for i in l:
        if isinstance(i,list):
            yield from flatten(i)
        else:
            yield i

def flip_map_key(map_key):
    key_list = map_key.split("-to-")
    key_list.reverse()
    return "-to-".join(key_list)

def is_hit(x, y):
    overlap = (max(x[0], y[0]), min(x[-1], y[-1])+1)
    return overlap[0] < overlap[1]

def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    seeds = re.findall(r"\d+", lines.pop(0))

    maps = {}
    for line in lines:          
        if "map:" in line:
            dict_key = line.replace(" map:", "")
            dict_key_reverse = flip_map_key(dict_key)
            maps[dict_key] = []
            maps[dict_key_reverse] = []
        elif line == "":
            pass
        else:
            dirty_nums = re.findall(r"\d+", line)
            destination_start = int(dirty_nums[0])
            source_start = int(dirty_nums[1])
            rng = int(dirty_nums[2])

            maps[dict_key].append({
                "destination_start": destination_start,
                "destination_end": destination_start + rng,
                "source_start": source_start,
                "source_end": source_start + rng
            })

    return maps, [int(x) for x in seeds]


class Maps():
    def __init__(self, maps):
        self.maps = maps

    def map_key(self, key, map_name, reverse=False):
        origin = "source"
        target = "destination"

        if reverse:
            origin = "destination"
            target = "source"

        lookups = list()
        for range in self.maps[map_name]:
            if range[f"{origin}_start"] <= key <= range[f"{origin}_end"]:
                lookups.append(key - range[f"{origin}_start"] + range[f"{target}_start"])
    
        match len(lookups):
            case 0:
                return key
            case 1:
                return lookups[0]
            case _:
                return lookups
        

    
    def traverse(self, key, level=0, reverse=False):
        if level > 6:
            return key

        index = 6 - level if reverse else level
        map_name = LOOKUP_ORDER[index]
        lookup = self.map_key(key, map_name, reverse)
        
        if isinstance(lookup, list):
            results = list()
            for l_key in lookup:
                results.append(self.traverse(l_key, level + 1, reverse))
            return results

        return self.traverse(lookup, level + 1, reverse)
    
    def range_traverse(self, x, level=0):
        if level > 6:
            return x
        
        map_name = LOOKUP_ORDER[level]
        mapping = self.maps[map_name]
        y_list = [ (y["source_start"], y["source_end"]) for y in mapping ]
        y_hits = [y for y in y_list if is_hit(x, y)]
        breakpoint()



def is_in_seed_range(seed, seed_ranges):
    return any([seed_range[0] <= seed < seed_range[1] for seed_range in seed_ranges])



def overlap_range(x, y):
    diff = (x[0] - y[0], x[1] - y[1])
    breakpoint()
    match (diff[0] < 0, diff[1] < 0):
        case (True, True):
            return x
        case (False, False):
            return x
        case _:
            overlap = (max(x[0], y[0]), min(x[-1], y[-1])+1)
    
    return (
        (min(x[0], overlap[0]), min(x[1], overlap[1])),
        (overlap),
        (max(x[0], overlap[0]), max(x[1], overlap[1]))
    )




if __name__ == "__main__":
    mappings, seeds = data("input.txt")
    maps = Maps(mappings)



    # Puzzle 1
    loc_list = list()
    for seed in seeds:
        results = maps.traverse(seed)
        loc_list.append(results)

    resulting_list = list(flatten(loc_list))
    print(f"Answer 1: {min(resulting_list)}")

    # Puzzle 2
    seed_ranges = list()
    loc_list = list()
    for num in range(len(seeds)//2):
        seed_start = seeds[num * 2]
        seed_range = seeds[num * 2 + 1]

        seed_ranges.append(
            (seed_start, seed_start + seed_range)
        )
    

    for seeds in seed_ranges:
        for seed in range(seeds[0], seeds[1]):
            results = maps.traverse(seed)
            loc_list.append(results)

    resulting_list = list(flatten(loc_list))
    print(f"Answer 2: {min(resulting_list)}")


    