import csv
import time

from app.SudokuExactCoverSolver import SudokuExactCoverSolver
from app.SudokuGenerator import SudokuGenerator
from app.SudokuValidator import SudokuValidator


def main(solver, n, csv_file=None):
    print('------------------')
    print(f'{solver.__name__} Solver')
    print('------------------')

    results = [('num_updates', 'time_taken', 'is_valid')]

    sudoku_generator = SudokuGenerator(n)
    sudoku_matrices = sudoku_generator.generate_puzzles()

    for sudoku_matrix in sudoku_matrices:
        num_updates, time_taken = solve_puzzle(solver, sudoku_matrix)
        sudoku_validator = SudokuValidator(sudoku_matrix)
        is_valid = sudoku_validator.validate()
        results.append((num_updates, time_taken, is_valid))

    if csv_file:
        write_data_to_csv(results, csv_file)
    else:
        [print(r) for r in results]

    return results


def solve_puzzle(solver, sudoku_matrix):
    start = time.time()
    s = solver(sudoku_matrix)
    s.solve()
    end = time.time()
    num_updates = s.get_num_updates()
    return num_updates, end - start


def write_data_to_csv(results, csv_file):
    with open(csv_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        [writer.writerow([r for r in result]) for result in results]


main(
    solver=SudokuExactCoverSolver,
    n=3
)
