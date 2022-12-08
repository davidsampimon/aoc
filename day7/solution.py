import os
from dataclasses import field, dataclass


class Drive(dict):
    def set_total_size(self, path="root"):
        total_size = self[path].size
        for child in self[path].children:
            child_path = f"{path}/{child}"
            total_size += self.set_total_size(child_path)
        self[path].total_size = total_size
        return total_size

@dataclass
class Dir:
    path: str
    size: int
    total_size: int
    children: list[int] = field(default_factory=list)

def get_context(command, path):
    dir = command[1]
    if dir == "..":
        path_parts = path.split("/")
        level_up = len(path_parts) - 1
        return os.path.join(*path_parts[:level_up])
    if dir == "/":
        return "root"
    else:
        return f"{path}/{dir}"

def check_exists(path, drive):
    return path in drive.keys()


if __name__ == "__main__":
    drive = Drive()
    pat = None
    
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    for row in total_lines:
        row_list = row.split()
        if row_list[1] == "cd":
            path = get_context(row_list[1:], path)
            if not check_exists(path, drive):
                drive[path] = Dir(path, 0, 0)
        if row_list[0].isnumeric():
            drive[path].size += int(row_list[0])
        if row_list[0] == "dir":
            drive[path].children.append(row_list[1])
    drive.set_total_size()

    ###### PUZZLE 1 #####
    results = []
    threshold = 100000
    for key, value in drive.items():
        if value.total_size <= threshold:
            results.append(value.total_size)
    print("####PUZZLE1####")
    print(sum(results))

    ###### PUZZLE 2 #####
    total_disk = 70000000
    space_needed = 30000000
    unused_space = total_disk - drive["root"].total_size
    to_delete = space_needed - unused_space
    results_two = []
    for key, value in drive.items():
        if value.total_size >= to_delete:
            results_two.append(value.total_size)
    results_two.sort()
    print("####PUZZLE2####")
    print(results_two[0])
