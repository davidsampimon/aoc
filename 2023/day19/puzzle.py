import operator

OPS = {
    "<": operator.lt,
    ">": operator.gt,
    "=": operator.eq,
}


def run_func(func, part):
    value = int(func[2:])
    return OPS[func[1]](part[func[0]], value)


def run_machine(machine, part):
    for component in machine:
        if run_func(component[0], part):
            return component[1]


def parse_func_line(line):
    results = list()
    parts = line.split(",")
    catch_all = ("x>0", parts.pop(-1))
    for func_string in parts:
        dirty_data = func_string.split(":")
        func = dirty_data[0]
        target = dirty_data[1]
        results.append(
            (func, target)
        )
    results.append(catch_all)
    return results


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    machines = dict()
    parts = list()
    for line in lines:
        if line == "":  continue
        if line[0] == "{":
            part = dict()
            line = line.replace("{", "").replace("}", "")
            data_list = line.split(",")
            for part_string in data_list:
                key_val = part_string.split("=")
                part[key_val[0]] = int(key_val[1])
            parts.append(part)
        else:
            name = line.split("{")[0]
            line = line[len(name):].replace("{", "").replace("}", "")
            machines[name] = parse_func_line(line)

    return machines, parts

if __name__ == "__main__":
    machines, parts = data("input.txt")
    for part in parts:
        machine = machines["in"]
        while machine:
            machine_name = run_machine(machine, part)
            if machine_name in "AR":
                part["status"] = machine_name
                machine = None
            else:
                machine = machines[machine_name]

    sum_total = 0
    for part in parts:
        if part["status"] == "A":
            sum_total += sum((part["x"], part["m"], part["a"], part["s"]))
    print(f"Answer 1: {sum_total}")
