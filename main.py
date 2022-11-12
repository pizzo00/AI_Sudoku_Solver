from time import process_time

from sudoku_constraints import SudokuConstraints
from sudoku_constraints_greedy import SudokuConstraintsGreedy


def main():
    # s = SudokuConstraintsGreedy(".62..417.84..1.........5.8......8..5....2.7.....9....42..67....4....1....175.26..")
    # s = SudokuConstraintsGreedy(".2....5938..5..46.94..6...8..2.3.....6..8.73.7..2.........4.38..7....6..........5")
    s = SudokuConstraintsGreedy("3...8.......7....51..............36...2..4....7...........6.13..452...........8..")

    print("\n")
    # Print initial sudoku
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

