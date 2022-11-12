from typing import Optional, List, Set, Tuple

from sudoku import Sudoku


class SudokuConstraints(Sudoku):

    def __init__(self, str_input: Optional[str] = None):
        self.__constraints: List[List[List[int]]] = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        super().__init__(str_input)

    def set(self, r: int, c: int, val: Optional[int]):
        # Nothing change
        if self.data[r][c] == val:
            return

        # Unset old constraints
        if self.data[r][c] is not None:
            self.__set_constraint(r, c, self.data[r][c], False)
        # Set new constraints
        if val is not None:
            self.__set_constraint(r, c, val, True)

        super().set(r, c, val)

    def _get_possible_values_for(self, r: int, c: int) -> Set[int]:
        out = set()
        for i in range(9):
            if self.__constraints[r][c][i] == 0:
                out.add(i + 1)

        return out

    def __set_constraint(self, row: int, col: int, val: int, insert: bool) -> None:
        inc = 1 if insert else -1

        # Row - Col
        for i in range(9):
            if i != col:
                self.__constraints[row][i][val - 1] += inc
            if i != row:
                self.__constraints[i][col][val - 1] += inc

        # Square
        sr = row // 3  # square row
        sc = col // 3  # square column
        for r in range(sr*3, sr*3 + 3):
            for c in range(sc*3, sc*3 + 3):
                # r = i + sr*3
                # c = j + sc*3
                if r != row and c != col:  # if cell is in the same row or col, will be already incremented
                    self.__constraints[r][c][val - 1] += inc

    def solve(self) -> bool:
        def func(r: int, c: int) -> bool:
            if r == 9:
                return True  # Reach bottom of recursion

            next_r, next_c = self.inc_row_col(r, c)
            if self.get(r, c) is not None:
                # Fixed number
                return func(next_r, next_c)
            else:
                choices = self._get_possible_values_for(r, c)
                for i in choices:
                    self.set(r, c, i)
                    if func(next_r, next_c):
                        return True
                self.set(r, c, None)

            return False  # Wrong solution
        return func(0, 0)
