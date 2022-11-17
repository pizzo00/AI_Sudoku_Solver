import copy
import math
import random
from typing import Optional, List, Set, Tuple

from sudoku import Sudoku

TOP_N = 100  # 250
INITIAL_COMBINATION_RATE = 98 / 100
INITIAL_MUTATION_RATE = 1 / 100
MUTATION_RATE_INC = 5 # / 1000  # 0.5%


class SudokuGenetic(Sudoku):
    class _NineChecker(Sudoku._NineChecker):
        def rank(self) -> int:
            return self.digits.count(False)

    __mutation_rate = INITIAL_MUTATION_RATE
    __combination_rate = INITIAL_COMBINATION_RATE

    def __init__(self, str_input: Optional[str] = None, initial_sudoku: Optional['SudokuGenetic'] = None, **kwargs):
        super().__init__(str_input, **kwargs)

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
        # return SudokuGenetic(repr(self), self.initial_sudoku or self)
        return SudokuGenetic(None, self.initial_sudoku or self, unsafe_init=copy.deepcopy(self.data))

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

        split = random.randrange(10, 70)
        out = [self.__clone(), partner.__clone()]

        if random.random() < self.initial_sudoku.__combination_rate:
            for r in range(9):
                for c in range(9):
                    if not self.__is_fixed_position(r, c):
                        if random.random() < self.initial_sudoku.__mutation_rate:
                            out[0].set(r, c, random.randrange(1, 10))
                            out[1].set(r, c, random.randrange(1, 10))
                        else:
                            if r*9 + c < split:
                                out[0].set(r, c, partner.get(r, c))
                                out[1].set(r, c, self.get(r, c))
        return out

    def solve(self):
        top_n = TOP_N
        gen = self.__get_first_gen(top_n * (top_n-1))
        gen.sort(key=lambda x: x.__rank_solution())

        last_rank = 10000000
        rank_age = 0
        while gen[0].__rank_solution() != 0:
            cur_rank = gen[0].__rank_solution()
            if cur_rank == last_rank:
                rank_age += 1
                self.__mutation_rate += MUTATION_RATE_INC
            else:
                self.__mutation_rate = INITIAL_MUTATION_RATE
                self.__combination_rate = INITIAL_COMBINATION_RATE
                rank_age = 0
            if rank_age > 5:
                self.__combination_rate = 1
            last_rank = cur_rank

            print(str(cur_rank) + " - " + str(self.__mutation_rate*100) + "%")
            print("\n")

            gen = gen[0:top_n]

            new_gen = []
            for i in range(0, top_n):
                for j in range(i+1, top_n):
                    new_gen += gen[i].__generate(gen[j])
            gen = new_gen
            gen.sort(key=lambda x: x.__rank_solution())

        self.data = gen[0].data  # I Won
        return True

