import itertools
from sys import argv

from termcolor import colored

try:
    NUM_OF_LETTERS = int(argv[1])
except IndexError:
    NUM_OF_LETTERS = 2

try:
    FILENAME = argv[2]
except IndexError:
    FILENAME = "automat6.txt"


def read_automat(filename) -> (list, list):
    ins = []
    outs = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            _ins = []
            for num in range(NUM_OF_LETTERS):
                _ins.append(line[num])
            ins.append(_ins)
            _outs = []
            for num in range(NUM_OF_LETTERS):
                _outs.append(line[NUM_OF_LETTERS + num])
            outs.append(_outs)
    return ins, outs


def print_automat(ins: list, outs: list) -> None:
    print(f" |{'abcdefghijklmnopqrstuvwxyz'[0:NUM_OF_LETTERS]}|{'abcdefghijklmnopqrstuvwxyz'[0:NUM_OF_LETTERS]}")
    print("-----------------")
    for i in range(len(ins)):
        print(f"{i + 1}|", end="")
        for num in range(NUM_OF_LETTERS):
            print(f"{ins[i][num]}", end="")
        print("|", end="")
        for num in range(NUM_OF_LETTERS):
            print(f"{outs[i][num]}", end="")
        print()


def make_triangle(ins: list, outs: list) -> (list, list):
    triangle = []
    xs = []
    for i in range(1, len(ins)):
        _tr = []
        for j in range(0, i):
            shall_break = False
            for num in range(NUM_OF_LETTERS):
                if outs[i][num] == '-' or outs[j][num] == '-':
                    pass
                elif outs[i][num] != outs[j][num]:
                    _tr.append('X')
                    _to_add = sorted([str(i), str(j)])
                    xs.append(f"{''.join(_to_add)}")
                    shall_break = True
                    break
            if shall_break:
                continue
            _full = ""
            for num in range(NUM_OF_LETTERS):
                if ins[i][num] == '-' or ins[j][num] == '-':
                    pass
                elif ins[i][num] != ins[j][num]:
                    _to_add = sorted([ins[i][num], ins[j][num]])
                    _full += f"{''.join(_to_add)}"
            if _full == "":
                _full = '√'
            _tr.append(_full)
        triangle.append(_tr)
    return triangle, xs


def print_triangle(triangle: list) -> None:
    for i in range(len(triangle)):
        print(f"{i + 2}", end="")
        for element in triangle[i]:
            if element == "X":
                element = colored(element + " " * (NUM_OF_LETTERS * 2 - 1), "red")
            if element == "√":
                element = colored(element + " " * (NUM_OF_LETTERS * 2 - 1), "green", attrs=["bold"])
            print(f"|{element}".ljust(NUM_OF_LETTERS * 2 + 1), end="")
        print()
    print(" ", end="")
    for i in range(len(triangle)):
        print(f"|{i + 1}".ljust(NUM_OF_LETTERS * 2 + 1), end="")
    print()


def delete_from_triangle(triangle: list, _i: int, _j: int):
    for i in range(0, len(triangle)):
        for j in range(0, i + 1):
            _to_comp = []
            for index in range(0, len(triangle[i][j]), 2):
                _to_comp.append(triangle[i][j][index:index + 2])
            if f"{_i + 1}{_j + 1}" in _to_comp:
                print(f"{i + 2}{j + 1} was deleted beacuse of \"X\" in {_j + 1}{_i + 1}")
                triangle[i][j] = "X"
                delete_from_triangle(triangle, j, i + 1)


def parse_triangle(triangle: list, xs: list) -> None:
    print("Filtering triangle...")
    for x in xs:
        delete_from_triangle(triangle, int(x[0]), int(x[1]))


def get_value_from_triangle(triangle: list) -> list:
    _list = []
    for i in range(len(triangle) - 1, -1, -1):
        for j in range(i + 1, len(triangle) + 1):
            if triangle[j - 1][i] != "X":
                _list.append(f"{i + 1}{j + 1}")
    return _list


def parse_value_from_triangle(triangle: list, values: list) -> list:
    _used = values.copy()
    _super = []
    for i in range(len(triangle) - 1, -1, -1):
        _likes_with = []
        print(f"{i + 1}|", end="")
        for val in _super:
            print(val, end=" ")
        for val in values:
            if val.startswith(f"{i + 1}"):
                _super.append(val)
                _likes_with.append(val[1])
                print(val, end=" ")
        for val in _used:
            if val.startswith(f"{i + 1}"):
                _likes_with.append(val[1])
        for val in _super:
            if not val.startswith(f"{i + 1}"):
                if all([n in _likes_with for n in val]):
                    for n in val:
                        for _to_del in _super:
                            if _to_del == f"{i + 1}{n}":
                                del _super[_super.index(_to_del)]
                    _super[_super.index(val)] = f"{i + 1}" + val

        print()
    return _super


def determine_full_coverage_possibilities(triangle: list, qs: list) -> list:
    _list = []
    for i in range(0, len(qs) + 1):
        for subset in itertools.combinations(range(len(qs)), i):
            _sub = []
            _ch = ""
            for _i in subset:
                _sub += qs[int(_i)]
                _ch += f"Q{_i + 1}"
            if all([str(n) in _sub for n in map(lambda x: x + 1, range(len(triangle) + 1))]):
                _list.append(_ch)
    if not _list:
        for _el in range(1, len(triangle) + 2):
            qs.append(str(_el))
        for i in range(0, len(qs) + 1):
            for subset in itertools.combinations(range(len(qs)), i):
                _sub = []
                _ch = ""
                for _i in subset:
                    _sub += qs[int(_i)]
                    _ch += f"Q{_i + 1}"
                if all([str(n) in _sub for n in map(lambda x: x + 1, range(len(triangle) + 1))]):
                    _list.append(_ch)
    return _list


def check_coverage(ins: list, outs: list, qs: list, _poss: str) -> bool:
    _all_qs = []
    for index in range(0, len(_poss), 2):
        _all_qs.append(_poss[index:index + 2])
    print("\nCHECKING POSSIBLE COVERAGE:", *_all_qs)
    print()
    print(" ", end="")
    for i in range(len(_all_qs)):
        print(f"|{_all_qs[i]}".ljust(len(qs[int(_all_qs[i][1]) - 1]) + 1), end="")
    print()
    print(" ", end="")
    for i in range(len(_all_qs)):
        print(f"|", *qs[int(_all_qs[i][1]) - 1], sep="", end="")
    print()
    print("-------------------")
    P = []
    for i in range(NUM_OF_LETTERS):
        P.append([])
        print("abcdefghijklmnopqrstuvwxyz"[i], end="")
        for j in range(len(_all_qs)):
            P[i].append([])
            print("|", end="")
            for num in qs[int(_all_qs[j][1]) - 1]:
                print(ins[int(num) - 1][i], end="")
                P[i][j].append(ins[int(num) - 1][i])
        print()
    print()
    print(f"  |{'abcdefghijklmnopqrstuvwxyz'[0:NUM_OF_LETTERS]}|{'abcdefghijklmnopqrstuvwxyz'[0:NUM_OF_LETTERS]}")
    print("-----------------")
    for i in range(len(_all_qs)):
        print(f"P{i + 1}|", end="")
        for j in range(NUM_OF_LETTERS):
            _row = P[j][i]
            _row = list(filter('-'.__ne__, _row))
            _any = False
            for x in range(len(_all_qs)):
                if all([n in qs[int(_all_qs[x][1]) - 1] for n in _row]):
                    _any = True
                    print(f"{x + 1}", end="")
                    break
            if not _any:
                print(colored('X', "red"))
                return False
        print("|", end="")
        for j in range(NUM_OF_LETTERS):
            _row = qs[int(_all_qs[i][1]) - 1]
            _l = ""
            for num in _row:
                _l2 = outs[int(num) - 1][j]
                if _l2 == '-':
                    continue
                if _l == "":
                    _l = _l2
                if _l == _l2:
                    continue
                print(colored('X', "red"))
                return False
            print(_l, end="")
        print()
    print()
    print(colored("AUTOMATE OK", "green"))
    return True


def main():
    ins, outs = read_automat(FILENAME)
    print("\nAUTOMATE:")
    print_automat(ins, outs)
    triangle, xs = make_triangle(ins, outs)
    print("\nTRIANGLE:")
    print_triangle(triangle)
    print()
    parse_triangle(triangle, xs)
    print("TRIANGLE FILTERED:")
    print_triangle(triangle)
    values = get_value_from_triangle(triangle)
    print("\nSEARCH:")
    parsed_qs = parse_value_from_triangle(triangle, values)
    print(colored(f"\n{' '.join(parsed_qs)}", "green"))
    print(*[f"Q{i + 1}" + " " * (len(parsed_qs[i]) - 2) for i in range(len(parsed_qs))])
    possibilities = determine_full_coverage_possibilities(triangle, parsed_qs)
    print("\nFULL COVERAGE POSSIBILITIES:")
    print(*possibilities)
    _i = 0
    while True:
        if check_coverage(ins, outs, parsed_qs, possibilities[_i]):
            break
        _i += 1


if __name__ == "__main__":
    main()
