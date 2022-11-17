from time import process_time

from sudoku_constraints import SudokuConstraints
from sudoku_constraints_greedy import SudokuConstraintsGreedy
from sudoku_genetic import SudokuGenetic


def main():
    # s = SudokuConstraints("6.9..2.41.....6...1..98...2.......96...3...7......12.8..31.4...2.......9.8...3...")
    s = SudokuConstraintsGreedy("3...8.......7....51..............36...2..4....7...........6.13..452...........8..")
    # s = SudokuGenetic("92.8716.5..36.49.2..52.9.8.4519..82.76.3.8.94.98.25...5..1..74.24..8.3.1.8.54..6.")

    # Print initial sudoku
    print("\n")
    print(str(s))
    print("------------------\n")

    start_time = process_time()
    res = s.solve()
    end_time = process_time()

    if res:
        # Print result
        print(str(s))
        print("Solved in ", end_time-start_time, "s")
        # Check correctness (ideally redundant)
        if not s.is_correct():
            print("ATTENTION SUDOKU NOT CORRECT!")
    else:
        print("Unsolvable")


if __name__ == '__main__':
    main()

