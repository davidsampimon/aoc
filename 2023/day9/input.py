import re


class DiffSeq():
    def __init__(self, original_list):
        self.seq_map = [original_list]
        self.diff_seq(original_list)
        self.predict()
        self.back_in_time()

    def diff_seq(self, num_list, layer=1):
        if all([x == 0 for x in num_list]):
            return

        diff_list = list()
        for index in range(len(num_list)-1):
            x = num_list[index]
            y = num_list[index + 1]
            diff_list.append(y-x)

        self.seq_map.append(diff_list)
        self.diff_seq(diff_list, layer+1)

    def predict(self):
        self.seq_map[-1].append(0)

        diff = 0
        for index in range(len(self.seq_map)-1, -1, -1):
            seq = self.seq_map[index]
            seq.append(seq[-1] + diff)
            diff = seq[-1]
    
    def back_in_time(self):
        self.seq_map[-1].append(0)

        diff = 0
        for index in range(len(self.seq_map)-1, -1, -1):
            seq = self.seq_map[index]
            seq.reverse()
            seq.append(seq[-1] - diff)
            diff = seq[-1]
            seq.reverse()


    def __repr__(self):
        return f"{self.seq_map}"


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    data_list = list()
    for line in lines:
        data_list.append([int(x) for x in re.findall(r"-?\d+", line)])

    return data_list


if __name__ == "__main__":
    oasis = data("input.txt")

    result = list()
    answer_one = 0
    answer_two = 0
    for seq in oasis:
        ds = DiffSeq(seq)
        result.append(ds)
        answer_one += ds.seq_map[0][-1]
        answer_two += ds.seq_map[0][0]

    print(f"Answer 1: {answer_one}")
    print(f"Answer 2: {answer_two}")
