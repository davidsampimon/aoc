possible_list_one = ["abc.txt", "xyz.txt"]
possible_list_two = ["abc.txt", None]

match possible_list:
    case [file1, file2]:
        print(file1, file2)
    case [file1, None]:
        print(file1)