import re


def solve(line, nums):
    memo = {}

    def func(i, n, b):
        """
        Returns how many solutions there are from this position
        i - index in line
        n - index in nums
        b - size of current block
        """
        if (i, n, b) in memo:
            return memo[(i, n, b)]

        if i == len(line):
            return int(
                (n == len(nums) and b == 0) or
                (n == len(nums) - 1 and b == nums[-1])
            )

        ans = 0
        if line[i] in ".?":
            if b == 0:
                ans += func(i+1, n, 0)
            else:
                if n == len(nums):
                    return 0
                if b == nums[n]:
                    ans += func(i+1, n+1, 0)

        if line[i] in "#?":
            ans += func(i+1, n, b+1)

        memo[(i, n, b)] = ans
        return ans
    return func(0, 0, 0)


def parse_line(line):
    line = re.sub(r"\.+", ".", line)
    data, nums = line.split()
    nums = eval(nums)

    return data, nums


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    return [parse_line(line) for line in lines]


if __name__ == "__main__":
    lines = data("input.txt")
    print(
        sum(solve(l, n) for l, n in lines)
    )

    lines_two = list()
    for line in lines:
        l, n = line
        lines_two.append(
            ("?".join([l] * 5), n*5)
        )
    print(
        sum(solve(l, n) for l, n in lines_two)
    )


#    #.?...### (1,1,3)