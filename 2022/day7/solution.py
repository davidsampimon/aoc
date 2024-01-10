import os


class Folder():
    def __init__(self, name):
        self.name = name
        self.size = 0
        self.children = set()

    @property
    def total_size(self):
        total_size = 0
        for child in self.children:
            total_size += child.total_size
        return self.size + total_size 
    
    def __repr__(self):
        return f"{self.name}: {self.total_size}"

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

def exist(path, drive):
    return path in drive.keys()


if __name__ == "__main__":
    drive = {"root": Folder("root")}
    path = None
    
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    for row in total_lines:
        row_list = row.split()
        if row_list[1] == "cd":
            path = get_context(row_list[1:], path)
        if row_list[0].isnumeric():
            drive[path].size += int(row_list[0])
        if row_list[0] == "dir":
            folder = row_list[1]
            if not exist(folder, drive):
                drive[f"{path}/{folder}"] = Folder(folder)
            drive[path].children.add(drive[f"{path}/{folder}"])

    ###### PUZZLE 1 #####
    result = 0
    threshold = 100000
    for key in drive.keys():
        if drive[key].total_size <= threshold:
            result += drive[key].total_size
    print("####PUZZLE1####")
    print(result)

    ###### PUZZLE 2 #####
    total_disk = 70000000
    space_needed = 30000000
    unused_space = total_disk - drive["root"].total_size
    to_delete = space_needed - unused_space
    results_two = []
    for key in drive.keys():
        if drive[key].total_size >= to_delete:
            results_two.append(drive[key].total_size)
    results_two.sort()
    print("####PUZZLE2####")
    print(results_two[0])
