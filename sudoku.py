import sys
from typing import Optional, List, Set, Tuple


class Sudoku:

    __stripValues = [' ', '\n', '\r', '\t']
    __acceptedValue = {str(i):i for i in range(1, 10)}

    def __init__(self):
        print("Please insert sudoku:\n")
        r = 0
        c = 0

        self.data: List[List[Optional[int]]] = [[None for _ in range(9)] for _ in range(9)]

        # char = sys.stdin.read(1) - Do not work for some reason
        user_input = ""
        while len(user_input) < 9*9:
            user_input += sys.stdin.readline()
            # Removed unwanted chars
            user_input = ''.join([c for c in user_input if c not in self.__stripValues])

        i = 0
        while r < 9:
            char = user_input[i]

            if char in self.__acceptedValue:
                self.set(r, c, self.__acceptedValue[char])
            else:
                self.set(r, c, None)

            i += 1
            r, c = self.inc_row_col(r, c)

    @staticmethod
    def inc_row_col(r, c) -> Tuple[int, int]:
        c += 1
        if c == 9:
            c = 0
            r += 1
        return r, c

    def get(self, r: int, c: int) -> Optional[int]:
        return self.data[r][c]

    def set(self, r: int, c: int, val: Optional[int]):
        self.data[r][c] = val

    def is_correct(self) -> bool:
        class NineChecker:
            def __init__(self):
                self.digits = [False for _ in range(9)]

            def set(self, digit: int):
                self.digits[digit-1] = True

            def is_correct(self) -> bool:
                return not (False in self.digits)

        # Check void positions
        for r in range(9):
            for c in range(9):
                if self.get(r, c) is None:
                    return False

        # Check rows
        for r in range(9):
            nc = NineChecker()
            for c in range(9):
                nc.set(self.get(r, c))
            if not nc.is_correct():
                return False

        # Check cols
        for c in range(9):
            nc = NineChecker()
            for r in range(9):
                nc.set(self.get(r, c))
            if not nc.is_correct():
                return False

        # Check squares
        for sr in range(3):  # square row
            for sc in range(3):  # square column
                nc = NineChecker()
                for r in range(sr*3, sr*3 + 3):
                    for c in range(sc*3, sc*3 + 3):
                        nc.set(self.get(r, c))
                if not nc.is_correct():
                    return False

        return True

    def __str__(self):
        out = "+---+---+---+\n"
        for r in range(9):
            out += "|"
            for c in range(9):
                out += str(self.get(r, c) or ".")
                if (c + 1) % 3 == 0:
                    out += "|"
            out += "\n"
            if (r + 1) % 3 == 0:
                out += "+---+---+---+\n"
        return out

    def __str2__(self):
        out = ""
        for r in range(9):
            for c in range(9):
                out += str(self.get(r, c) or ".")
                if (c+1) % 3 == 0:
                    out += " "
            out += "\n"
            if (r+1) % 3 == 0:
                out += "\n"
        return out
