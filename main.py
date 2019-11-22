import csv
import time

from app.SudokuBackTrackingSolver import SudokuBackTrackingSolver
from app.SudokuExactCoverSolver import SudokuExactCoverSolver
from app.SudokuGenerator import SudokuGenerator
from app.SudokuValidator import SudokuValidator


def run_exact_cover_solver():
    main(
        solver=SudokuExactCoverSolver,
        n=3,
        num_puzzles=10
    )


def run_backtracking_solver():
    main(
        solver=SudokuBackTrackingSolver,
        n=3,
        num_puzzles=10,
        write_to_csv=True
    )


def main(solver, n, num_puzzles=None, write_to_csv=False):
    print('------------------')
    print(f'{solver.__name__}')
    print('------------------')

    results = [('num_updates', 'time_taken', 'is_valid')]

    sudoku_generator = SudokuGenerator(n)
    sudoku_matrices = sudoku_generator.generate_puzzles(num_puzzles)
    # sudoku_matrices = sudoku_generator.generate_puzzle_from_id(1001)

    for sudoku_matrix in sudoku_matrices:
        num_updates, time_taken = solve_puzzle(solver, sudoku_matrix)
        sudoku_validator = SudokuValidator(sudoku_matrix)
        is_valid = sudoku_validator.validate()
        results.append((num_updates, time_taken, is_valid))

    if write_to_csv:
        write_data_to_csv(results, f'output/sudoku_rank_{n}_{solver.__name__}.csv')
    else:
        [print(r) for r in results]

    return results


def solve_puzzle(solver, sudoku_matrix):
    s = solver(sudoku_matrix)

    start = time.time()
    s.solve()
    end = time.time()
    num_updates = s.get_num_updates()
    return num_updates, end - start


def write_data_to_csv(results, csv_file):
    with open(csv_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        [writer.writerow([r for r in result]) for result in results]


run_exact_cover_solver()
