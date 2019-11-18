import csv
import time

from SudokuBackTrackingSolver import SudokuBackTrackingSolver
from SudokuExactCoverSolver import SudokuExactCoverSolver
from SudokuGenerator import SudokuGenerator
from SudokuValidator import SudokuValidator


def main(solver):
    # Generate Sudoku Matrices
    sudoku_generator = SudokuGenerator()
    sudoku_matrices = sudoku_generator.generate_puzzles(num_puzzles=1)

    # Create csv file to write output
    with open(f'output/results_{solver.__name__}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['time_taken'])

        # Solve Sudoku Puzzle
        for i, sudoku_matrix in enumerate(sudoku_matrices):
            print(f'Solving sudoku_matrix_{i}')
            time_taken = solve_puzzle(solver, sudoku_matrix)

            # Validate Sudoku Solution
            sudoku_validator = SudokuValidator(sudoku_matrix)
            is_valid = sudoku_validator.validate()
            # assert is_valid
            if not is_valid:
                print(f'SOLUTION FOR SUDOKU MATRIX {i} NOT VALID')

            # Write result to csv
            writer.writerow([time_taken])


def solve_puzzle(solver, sudoku_matrix):
    start = time.time()
    solver(sudoku_matrix).solve()
    end = time.time()
    return end - start


print('------------------')
print('Exact Cover Solver')
print('------------------')
main(solver=SudokuExactCoverSolver)

print('------------------')
print('Backtracking Solver')
print('------------------')
main(solver=SudokuBackTrackingSolver)
