from enum import Enum
from typing import Optional, List, Set, Tuple

from sudoku_constraints import SudokuConstraints


class SudokuConstraintsGreedy(SudokuConstraints):

    def __init__(self, str_input: Optional[str] = None):
        super().__init__(str_input)

    class __NextStep(Enum):
        NotFound = 1
        FoundZero = 2
        Found = 3

    def __get_next_step(self) -> Tuple[__NextStep, Optional[Tuple[int, int]]]:
        min_val = 10  # Max is 9
        min_out = (None, None)
        for r in range(9):
            for c in range(9):
                if self.get(r, c) is None:
                    val = self.get_possible_values_for(r, c)
                    if len(val) < min_val:
                        min_val = len(val)
                        min_out = (r, c)
        if min_val == 0:
            return self.__NextStep.FoundZero, None
        if min_val == 10:
            return self.__NextStep.NotFound, None
        return self.__NextStep.Found, min_out

    def solve(self) -> bool:
        next_step = self.__get_next_step()
        if next_step[0] == self.__NextStep.FoundZero:
            return False  # Wrong solution
        if next_step[0] == self.__NextStep.NotFound:
            return True  # Reach bottom of recursion

        r, c = next_step[1]

        choices = self.get_possible_values_for(r, c)
        for i in choices:
            self.set(r, c, i)
            if self.solve():
                return True
        self.set(r, c, None)

        return False  # Wrong solution
