

def hash(string):
    """
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """

    current_value = 0

    for char in string:
        ascii = ord(char)
        current_value += ascii
        current_value = current_value * 17
        current_value = current_value % 256

    return current_value


def data(filepath):
    with open(filepath, "r") as f:
        data_list = f.read().split(",")
    return data_list


if __name__ == "__main__":
    # test hashing on HASH
    assert hash("HASH") == 52

    # puzzle 1
    input_list = data("input.txt")
    answer = 0

    for string in input_list:
        answer += hash(string)
    print(f"Answer 1: {answer}")
