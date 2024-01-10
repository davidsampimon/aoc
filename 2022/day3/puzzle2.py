from day5.puzzle1 import calc_prio


def intersec_of_sets(group_list):
    s1 = set(group_list[0])
    s2 = set(group_list[1])
    s3 = set(group_list[2])

    set1 = s1.intersection(s2)
    result_set = set1.intersection(s3)
    if len(result_set) > 1:
        raise Exception("Multiple badges found")

    return result_set.pop()

if __name__ == "__main__":
    total_badge_prio = 0

    with open("input.txt", "r") as f:
        line_list = f.read().splitlines() 
        total_lines = len(line_list)
        for index in range(int(total_lines/3)):
            start_line = index * 3
            end_line = (index + 1) * 3
            badge = intersec_of_sets(line_list[start_line: end_line])
            total_badge_prio += calc_prio(badge)
    
    print(total_badge_prio)