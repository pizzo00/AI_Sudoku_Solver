import math
import random
from typing import Optional, List, Set, Tuple

from sudoku import Sudoku


class SudokuGenetic(Sudoku):
    class _NineChecker(Sudoku._NineChecker):
        def rank(self) -> int:
            return self.digits.count(False)

    __top_n = 80

    def __init__(self, str_input: Optional[str] = None, initial_sudoku: Optional['SudokuGenetic'] = None):
        super().__init__(str_input)

        self.__rank: Optional[int] = None
        self.initial_sudoku = initial_sudoku
        self.is_initial_sudoku = self.initial_sudoku is None
        if self.is_initial_sudoku:
            self.fixed_pos: Set[Tuple[int, int]] = set()
            for r in range(9):
                for c in range(9):
                    if self.get(r, c) is not None:
                        self.fixed_pos.add((r, c))

    def __is_fixed_position(self, r: int, c: int) -> bool:
        if self.is_initial_sudoku:
            return (r, c) in self.fixed_pos
        return self.initial_sudoku.__is_fixed_position(r, c)

    def __clone(self) -> 'SudokuGenetic':
        return SudokuGenetic(repr(self), self.initial_sudoku or self)

    def __rank_solution(self) -> int:
        if self.__rank is not None:
            return self.__rank

        rank = 0
        # Check rows
        for r in range(9):
            nc = SudokuGenetic._NineChecker()
            for c in range(9):
                nc.set(self.get(r, c))
            rank += nc.rank()

        # Check cols
        for c in range(9):
            nc = SudokuGenetic._NineChecker()
            for r in range(9):
                nc.set(self.get(r, c))
            rank += nc.rank()

        # Check squares
        for sr in range(3):  # square row
            for sc in range(3):  # square column
                nc = SudokuGenetic._NineChecker()
                for r in range(sr * 3, sr * 3 + 3):
                    for c in range(sc * 3, sc * 3 + 3):
                        nc.set(self.get(r, c))
                rank += nc.rank()

        self.__rank = rank
        return rank

    def __get_first_gen(self, size: int) -> List['SudokuGenetic']:
        out: List[SudokuGenetic] = [self.__clone() for _ in range(size)]
        for r in range(9):
            for c in range(9):
                if not self.__is_fixed_position(r, c):
                    for s in out:
                        s.set(r, c, random.randrange(1, 10))  # TODO think abut a seed or secret class
        return out

    def __generate(self, partner: 'SudokuGenetic') -> List['SudokuGenetic']:
        split = (9*9) // 2

        split = random.randrange(15, 65)
        out = [self.initial_sudoku.__clone(), self.initial_sudoku.__clone()]
        for r in range(9):
            for c in range(9):
                if not self.__is_fixed_position(r, c):
                    if r*9 + c < split:
                        out[0].set(r, c, self.get(r, c))
                        out[1].set(r, c, partner.get(r, c))
                    else:
                        out[0].set(r, c, partner.get(r, c))
                        out[1].set(r, c, self.get(r, c))
        return out

    def solve(self):
        top_n = self.__top_n
        gen = self.__get_first_gen(top_n * (top_n-1) // 2)
        gen.sort(key=lambda x: x.__rank_solution())

        while gen[0].__rank_solution() != 0:
            print(gen[0].__rank_solution())
            print("\n")

            gen = gen[0:top_n]
            random.shuffle(gen)  # TODO maybe I should remove it

            new_gen = []
            for i in range(0, top_n):
                for j in range(i+1, top_n):
                    new_gen += gen[i].__generate(gen[j])
            gen = new_gen
            gen.sort(key=lambda x: x.__rank_solution())

        return gen[0]  # I Won

