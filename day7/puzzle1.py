import os


def is_command(line):
    return line[0] == "$"        

def get_command(line):
    command_list = line.split()
    return command_list[1:]

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

def set_total_size(disk_dict, path="root"):
    total_size = disk_dict[path]["size"]
    for child in disk_dict[path]["children"]:
        child_path = f"{path}/{child}"
        total_size += set_total_size(disk_dict, child_path)
    disk_dict[path]["total_size"] = total_size
    return total_size


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    disk_dict = {}
    path = None
    command = [None]
    path = "root"
    result = []
    for line in total_lines:
        if is_command(line):
            if command[0] == "ls":
                disk_dict[path] = {
                    command[0]: result,
                    "children": [],
                    "total_size": 0
                    }
                result = []
            command = get_command(line)
            match command[0]:
                case "cd":
                    path = get_context(command, path)
                case "ls":
                    pass
                case _:
                    raise Exception(f"Unknown command {command}")
        else:
            result.append(line)
    disk_dict[path] = {
        command[0]: result,
        "children": [],
        "total_size": 0
    }

    for key, value in disk_dict.items():
        size = 0
        for string in value["ls"]:
            if string.split()[0].isnumeric():
                size += int(string.split()[0])
            elif "dir" in string:
                child = string.split()[1]
                if "children" in disk_dict[key].keys():
                    disk_dict[key]["children"].append(child)
                else:
                    disk_dict[key]["children"] = [child]

        disk_dict[key]["size"] = size
    set_total_size(disk_dict)


    ###### PUZZLE 1 #####
    results = []
    threshold = 100000
    for path, value in disk_dict.items():
        if value["total_size"] <= threshold:
            results.append(value["total_size"])
    print("####PUZZLE1####")
    print(sum(results))
    

    ###### PUZZLE 2 #####
    total_disk = 70000000
    space_needed = 30000000
    unused_space = total_disk - disk_dict["root"]["total_size"]
    to_delete = space_needed - unused_space
    results_two = []
    for key, value in disk_dict.items():
        if value["total_size"] >= to_delete:
            results_two.append(value["total_size"])
    print("####PUZZLE2####")
    results_two.sort()
    print(results_two[0])
