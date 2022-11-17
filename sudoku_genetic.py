import copy
import math
import random
from typing import Optional, List, Set, Tuple

from sudoku import Sudoku

GEN_N = 4000
ELITE_N = int(GEN_N * (5/100))
CANDIDATE_N = int(GEN_N * (70/100))
INITIAL_COMBINATION_RATE = 98 / 100
INITIAL_MUTATION_RATE = 1 / 100


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
            self.__fixed_pos: Set[Tuple[int, int]] = set()
            self.__free_positions: List[List[int]] = [[] for _ in range(0, 9)]
            self.__free_digits: List[List[int]] = [[] for _ in range(0, 9)]
            for r in range(9):
                free_digit = [i for i in range(1, 10)]
                for c in range(9):
                    if self.get(r, c) is not None:
                        self.__fixed_pos.add((r, c))
                        free_digit.remove(self.get(r, c))
                    else:
                        self.__free_positions[r].append(c)
                self.__free_digits[r] = free_digit

    def __is_fixed_position(self, r: int, c: int) -> bool:
        if self.is_initial_sudoku:
            return (r, c) in self.__fixed_pos
        return self.initial_sudoku.__is_fixed_position(r, c)

    def __clone(self) -> 'SudokuGenetic':
        # return SudokuGenetic(repr(self), self.initial_sudoku or self)
        return SudokuGenetic(None, self.initial_sudoku or self, unsafe_init=copy.deepcopy(self.data))

    def __rank_solution(self, recalculate=False) -> int:
        if not recalculate and self.__rank is not None:
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
            for s in out:
                d = 0
                free_digit = self.__free_digits[r]
                random.shuffle(free_digit)
                for c in self.__free_positions[r]:
                    s.set(r, c, free_digit[d])
                    d += 1
        return out

    def __get_parent(self, candidates: List['SudokuGenetic']):
        i1 = random.randrange(0, CANDIDATE_N)
        i2 = random.randrange(0, CANDIDATE_N)
        while i1 == i2:
            i2 = random.randint(0, len(candidates)-1)

        s1 = candidates[i1]
        s2 = candidates[i2]

        if s1.__rank_solution() > s2.__rank_solution():
            best, worst = s1, s2
        else:
            best, worst = s2, s1

        if random.random() < self.__combination_rate:
            return best
        else:
            return worst

    def __generate(self, partner: 'SudokuGenetic') -> Tuple['SudokuGenetic', 'SudokuGenetic']:
        out = (self.__clone(), partner.__clone())

        split_r_s = random.randint(0, 9)
        split_r_e = random.randint(0, 9)
        if split_r_s > split_r_e:
            split_r_s, split_r_e = split_r_e, split_r_s

        for r in range(9):
            free_digit = self.initial_sudoku.__free_digits[r]
            random.shuffle(free_digit)
            digits_to_be_changed = free_digit[0:random.randrange(0, len(free_digit))]
            digit1: List[int] = []
            digit2: List[int] = []
            for c in range(9):
                d1 = self.get(r, c)
                d2 = partner.get(r, c)
                if d1 in digits_to_be_changed:
                    digit1.append(d1)
                if d2 in digits_to_be_changed:
                    digit2.append(d2)
            for c in range(9):
                if self.get(r, c) in digits_to_be_changed:
                    self.set(r, c, digit2.pop(0))
                if partner.get(r, c) in digits_to_be_changed:
                    partner.set(r, c, digit1.pop(0))
        return out

    def __mutate(self):
        to_be_mutated = random.random() < self.initial_sudoku.__mutation_rate

        if to_be_mutated:
            r = random.randint(0, 8)
            free_pos = self.initial_sudoku.__free_positions[r]
            c1 = random.randrange(0, len(free_pos))
            c2 = random.randrange(0, len(free_pos))

            temp = self.get(r, c1)
            self.set(r, c1, self.get(r, c2))
            self.set(r, c2, temp)

        return to_be_mutated

    def solve(self):
        gen = self.__get_first_gen(GEN_N)
        gen.sort(key=lambda x: x.__rank_solution())

        gen_n = 0
        while gen[0].__rank_solution() != 0:
            cur_rank = gen[0].__rank_solution()

            gen_n += 1
            print("Fitness: " + str(cur_rank) + ", Generation: " + str(gen_n))
            print("\n")

            # keep elite
            new_gen = gen[0:ELITE_N]
            candidates = gen[0:CANDIDATE_N]

            num_of_mutations = 0
            successful_mutations = 0
            while len(new_gen) < GEN_N:
                p1 = self.__get_parent(candidates)
                p2 = self.__get_parent(candidates)
                c1, c2 = p1.__generate(p2)

                # Mutate
                c1_old_rank = c1.__rank_solution()
                c2_old_rank = c2.__rank_solution()
                if c1.__mutate():
                    num_of_mutations += 1
                    if c1.__rank_solution(recalculate=True) < c1_old_rank:
                        successful_mutations += 1
                if c2.__mutate():
                    num_of_mutations += 1
                    if c2.__rank_solution(recalculate=True) < c2_old_rank:
                        successful_mutations += 1

                # Append
                new_gen.append(c1)
                new_gen.append(c2)

            gen = new_gen
            gen.sort(key=lambda x: x.__rank_solution())

            # Rechenberg's 1/5 rule
            if num_of_mutations != 0:
                rate_of_successful_mutations = successful_mutations / num_of_mutations
                if rate_of_successful_mutations < (1/5):
                    self.__mutation_rate *= 0.95
                elif rate_of_successful_mutations > (1/5):
                    self.__mutation_rate /= 0.95
            else:
                self.__mutation_rate *= 2

        self.data = gen[0].data  # I Won
        return True

