from sudoku_constraints import SudokuConstraints


def solve(s: SudokuConstraints, r: int, c: int) -> bool:
    if r == 9:
        return True  # Reach bottom of recursion

    next_r, next_c = SudokuConstraints.inc_row_col(r, c)
    if s.get(r, c) is not None:
        # Fixed number
        return solve(s, next_r, next_c)
    else:
        choices = s.get_possible_values_for(r, c)
        for i in choices:
            s.set(r, c, i)
            if solve(s, next_r, next_c):
                return True
        s.set(r, c, None)

    return False  # Unsolvable


def main():
    s = SudokuConstraints()

    print("\n")
    # Print initial sudoku
    print(str(s))
    print("-------------------------------------------\n")

    if solve(s, 0, 0):
        print("Solved")
        # Print result
        print(str(s))
        # Check correctness (ideally redundant)
        print("Correct" if s.is_correct() else "ATTENTION SUDOKU NOT CORRECT!")
    else:
        print("Unsolvable")


if __name__ == '__main__':
    main()

