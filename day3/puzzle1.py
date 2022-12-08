OFFSET_UPPER = 38
OFFSET_LOWER = 96

def parse_row(dirty_row):
    row = dirty_row.strip()
    split_num = int(len(row)/2)
    compartment_one = row[:split_num]
    compartment_two = row[split_num:]
    return compartment_one, compartment_two

def print_example(compartment_one, compartment_two, char):
    print(f"{compartment_one} | {compartment_two}")
    print(f"{char}: score {prio_score}")
    print("###")

def calc_prio(char):
    if char.isupper():
        return ord(char) - OFFSET_UPPER
    else:
        return ord(char) - OFFSET_LOWER


if __name__ == "__main__":
    total_prio = 0
    print_examples = 3

    with open("input.txt", "r") as f:
        for index, dirty_row in enumerate(f):
            compartment_one, compartment_two = parse_row(dirty_row)
            for char in set(compartment_one):
                if char in compartment_two:
                    prio_score = calc_prio(char)
                    if index < print_examples:
                        print(
                            compartment_one,
                            compartment_two,
                            char,
                            prio_score
                        )
                    total_prio += prio_score

    print("###ANSWER PUZZLE1 ###")
    print(total_prio)

