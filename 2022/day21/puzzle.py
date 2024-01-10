import time

def find_value(key, data_dict):
    value = data_dict[key]
    match value:
        case int():
            return value
        case dict():
            a = find_value(value["a"], data_dict)
            b = find_value(value["b"], data_dict)
            operator = value["operator"]
            return eval(f"{a} {operator} {b}")
        case _:
            raise TypeError("Invalid type")

def inverse_find(key, target_key, data_dict, solution=0):
    if key == target_key:
        return solution

    value = data_dict[key]
    match value:
        case int():
            return value
        case dict():
            a_val, b_val = path_finder(key, data_dict)
            solve_for, solution_ = invert_algebra(
                a_val,
                b_val,
                solution, 
                value["operator"]
            )
            return inverse_find(solve_for, target_key, data_dict, solution_)

def invert_algebra(a_val, b_val, solution, operator):
    match operator:
        case "==":
            if isinstance(a_val, str):
                path = a_val
                solution_ = b_val
            else:
                path = b_val
                solution_ = a_val
            return path, solution_
        case "*":
            if isinstance(a_val, str):
                path = a_val
                solution_ = eval(f"{solution} / {b_val}")
            else:
                path = b_val
                solution_ = eval(f"{solution} / {a_val}")
            return path, solution_  
        case "+":
            if isinstance(a_val, str):
                path = a_val
                solution_ = eval(f"{solution} - {b_val}")
            else:
                path = b_val
                solution_ = eval(f"{solution} - {a_val}")
            return path, solution_  
        case "-":
            if isinstance(a_val, str):
                path = a_val
                solution_ = eval(f"{solution} + {b_val}")
            else:
                path = b_val
                solution_ = eval(f"{a_val} - {solution}")
            return path, solution_
        case "/":
            if isinstance(a_val, str):
                path = a_val
                solution_ = eval(f"{solution} * {b_val}")
            else:
                path = b_val
                solution_ = eval(f"{a_val} / {solution}")
            return path, solution_
        case _:
            raise Exception(f"Unknown operator {operator}")

def path_finder(key, data_dict):
    root_a = data_dict[key]["a"]
    root_b = data_dict[key]["b"]
    try:
        a_val = find_value(root_a, data_dict)
        b_val = root_b
    except:
        a_val = root_a
        b_val = find_value(root_b, data_dict)
    return a_val, b_val

def parse_input(data):
    with open(data, "r") as f:
        line_list = f.read().splitlines()
    
    results = {}
    for row in line_list:
        parts = row.split(":")
        key = parts[0]
        func = parts[1].split()
        if len(func) == 1:
            results[key] = int(func[0])
        else:
            a = func[0]
            operator = func[1]
            b = func[2]
            results[key] = {
                "a" : a,
                "operator": operator,
                "b" : b
            }
    return results

def main():
    input_dict = parse_input("input.txt")
    
    # puzzle 1
    root = find_value("root", input_dict)
    print(int(root))

    # puzzle 2
    input_dict["root"]["operator"] = "=="
    input_dict["humn"] = "#"
    answer_two = inverse_find("root", "humn", input_dict)
    print(answer_two)

if __name__ == "__main__":
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f"Execution time: {t2 - t1:0.4f} seconds")
