from __future__ import annotations

import argparse
import random
import sys
from collections import Counter

from .solver import WordleSolver, read_dictionary


def get_command_line_args() -> argparse.Namespace:
    """
    Parse command line arguments and return a namespace object.

    Returns:
        argparse.Namespace: A namespace object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Wordle solver")
    parser.add_argument(
        "--solve", action="store_true", help="Solve a Wordle puzzle based on feedback"
    )
    parser.add_argument(
        "--bench", action="store_true", help="Benchmark the Wordle solver"
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def solve_wordle_puzzle(full_dictionary: list[str]) -> int:
    """
    Solves the Wordle puzzle by taking user input and filtering the solution
    space.

    Returns:
        The number of guesses taken to solve the puzzle.
    """
    solver = WordleSolver(full_dictionary)
    print(f"Solution space size: {len(solver.solution_space)}")
    print(
        """
Legend:
g - green
y - yellow
x - grey (missed)
          """
    )

    guess_count = 0

    # Continue guessing until the solution space is reduced to a single word
    while len(solver.solution_space) > 1:
        # Suggest the best guess to the user.
        best_guess = solver.get_best_guess()
        if best_guess:
            print(f"Suggested guess: {best_guess}")

        while True:
            guess = input("What was your guess: ")
            if len(guess) == 5:
                break
            print("Error: Guess must be 5 letters long.", file=sys.stderr)

        while True:
            result = input("What was your result (e.g., 'gyyxx'): ")
            if len(result) == 5 and all(c in "gyx" for c in result):
                break
            print(
                "Error: Result must be 5 characters and only contain"
                " 'g', 'y', or 'x'.",
                file=sys.stderr,
            )

        solver.filter_solution(guess, result)
        guess_count += 1

        print(f"Solution space size: {len(solver.solution_space)}")
        print(f"Solution space: {solver.solution_space}")
    return guess_count + 1


def benchmarking_solver(full_dictionary: list[str]) -> None:
    """
    Benchmarks the Wordle solver by running it multiple times
    and printing the average number of guesses and the maximum number of
    guesses.
    """
    iterations = 10000
    guess_counts: Counter[int] = Counter()
    failures = 0
    for _ in range(iterations):
        solver = WordleSolver(full_dictionary)
        answer = random.choice(full_dictionary)
        try:
            num_guesses = solver.solve(answer)
            guess_counts[num_guesses] += 1
        except RuntimeError:
            # You could log the error `e` here if desired
            failures += 1

    if guess_counts:
        total_solves = sum(guess_counts.values())
        total_guesses = sum(k * v for k, v in guess_counts.items())
        average_guesses = total_guesses / total_solves
        max_guesses = max(guess_counts.keys())
        print(
            f"Average: {average_guesses:.2f} guesses (max: {max_guesses}) "
            f"on {total_solves} successful solves."
        )
        print("\nGuess Distribution:")
        for i in sorted(guess_counts.keys()):
            count = guess_counts[i]
            percentage = (count / total_solves) * 100
            print(f"  Solved in {i} guesses: {count:<5} ({percentage:.2f}%)")
    else:
        print("No puzzles were solved successfully.")

    if failures > 0:
        print(f"Failed to solve {failures} puzzles out of {iterations}.")


def main() -> None:
    """Command-line entry point."""
    args = get_command_line_args()
    try:
        full_dictionary = read_dictionary()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print(
            f"Dictionary not found. Please ensure '{e.filename}' is in the current"
            " directory.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.bench:
        benchmarking_solver(full_dictionary)

    if args.solve:
        guess_count = solve_wordle_puzzle(full_dictionary)
        print(f"The puzzle was solved in {guess_count} guesses.")
