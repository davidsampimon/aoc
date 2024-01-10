from math import log


char_map = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2
}

value_map = dict(map(reversed, char_map.items()))

def snafu(row):
    value = 0
    for index, char in enumerate(reversed(row)):
        value += 5 ** index * char_map[char]
    return value

def isnafu(digits):
    output = ""
    while digits:
        rem = digits % 5
        digits //= 5
        if rem <=2:
            output = str(rem) + output
        else:
            output = "   =-"[rem] + output
            digits += 1


    return output


def parse_input(data):
    with open(data, "r") as f:
        row_input = f.read().splitlines()
    return row_input


def main():
    rows = parse_input("input.txt")
    answers = []
    for row in rows:
        answers.append(snafu(row))
    
    answer_one = sum(answers)
    answer_two = isnafu(answer_one)
    print(f"Sum is {answer_one} in SNAFU is {answer_two}")

if __name__ == "__main__":
    main()