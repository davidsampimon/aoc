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

def is_valid_range(rng):
    return rng[0] < rng[1]

def split_range(rng, split, start=True):
    bottom = rng[0]
    top = rng[1]
    results = list()

    if bottom <= split <= top:
        if start:
            if is_valid_range((bottom, split-1)):
                results.append((bottom, split-1))
            results.append((split, top))
        else:
            results.append((bottom, split))
            if is_valid_range((split+1, top)):
                results.append((split+1, top))
        return results
    else:
        return [rng]



def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    seeds = re.findall(r"\d+", lines.pop(0))
    seeds = [int(x) for x in seeds]
    seed_ranges = list()

    for num in range(len(seeds)//2):
        seed_start = seeds[num * 2]
        seed_range = (seeds[num * 2 + 1] - 1)

        seed_ranges.append(
            (seed_start, seed_start + seed_range)
        )

    maps = {}
    for line in lines:          
        if "map:" in line:
            dict_key = line.replace(" map:", "")
            maps[dict_key] = []
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

    return maps, seed_ranges

class SR():
    def __init__(self, maps):
        self.maps = maps

    def traverse_range(self, ranges, level=0):

        map = self.maps[LOOKUP_ORDER[level]]
        splits = [(x["source_start"], x["source_end"]) for x in map]

        new_ranges = set()
        breakpoint()
        for split in splits:
            for range in ranges:
                range = split_range(range, split[0])
                range = split_range(range, split[1], start=False)
        
        out_ranges = set()
        for range in new_ranges:
            out_ranges.add(self.transpose(range, map))

        return self.traverse_range(out_ranges, level+1)

    def transpose(self, range, map):
        check_num = range[0]

        for map_dict in map:
            if map_dict["source_start"] <= check_num <= map_dict["source_start"]:
                range = (
                    range[0] - map_dict["source_start"] + map_dict["destination_start"],
                    range[1] - map_dict["source_start"] + map_dict["destination_start"],
                )
        
        return range




if __name__ == "__main__":
    maps, seeds = data("test.txt")

    sr = SR(maps)


    split_range((55, 67), 61, start=False)



    sr.traverse_range(seeds)
    breakpoint()



    print(split_range((0, 10), 6))