import sys
from typing import Optional, List, Set, Tuple

from sudoku import Sudoku


class SudokuConstraints(Sudoku):

    def __init__(self):
        self.__constraints: List[List[List[int]]] = [[[0 for _ in range(9)] for _ in range(9)] for _ in range(9)]
        super().__init__()

    def set(self, r: int, c: int, val: Optional[int]):
        # Nothing change
        if self.data[r][c] == val:
            return

        # Unset old constraints
        if self.data[r][c] is not None:
            self.set_constraint(r, c, self.data[r][c], False)
        # Set new constraints
        if val is not None:
            self.set_constraint(r, c, val, True)

        super().set(r, c, val)

    def get_possible_values_for(self, r: int, c: int) -> Set[int]:
        out = set()
        for i in range(9):
            if self.__constraints[r][c][i] == 0:
                out.add(i + 1)

        return out

    def set_constraint(self, row: int, col: int, val: int, insert: bool) -> None:
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
