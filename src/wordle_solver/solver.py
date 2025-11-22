from __future__ import annotations

import copy
import os
from collections import Counter

DEFAULT_DICTIONARY_FILE = "english-usa-dictionary.txt"


def read_dictionary(source_file_dictionary: str = DEFAULT_DICTIONARY_FILE) -> list[str]:
    """
    Reads the reduced USA ENGLISH dictionary from the file `english-usa-dictionary.txt`.

    Returns:
        A list of words, each of which is 5 characters long.
    """

    dictionary = []
    try:
        with open(os.path.join(os.getcwd(), source_file_dictionary), "r") as f:
            for line in f:
                word = line.rstrip()
                if len(word) == 5:
                    dictionary.append(word)
    except FileNotFoundError:
        # Let the caller (the CLI) handle the user-facing error message and exit,
        # making this function more reusable.
        raise
    return dictionary


class WordleSolver:
    def __init__(self, full_dictionary: list[str]) -> None:
        self.full_dictionary = full_dictionary
        self.solution_space = copy.deepcopy(self.full_dictionary)

    @staticmethod
    def generate_result(guess: str, answer: str) -> str:
        """
        Generates the result of a Wordle guess, handling duplicate letters correctly.

        'g' for correct letter in correct position.
        'y' for correct letter in wrong position.
        'x' for incorrect letter (miss).

        Args:
            guess: The guessed word.
            answer: The correct word.

        Returns:
            A 5-character string representing the result (e.g., 'ygxxy').
        """
        result = [""] * 5
        answer_counts = Counter(answer)

        # First pass for green letters (correct letter and position)
        for i, letter in enumerate(guess):
            if answer[i] == letter:
                result[i] = "g"
                answer_counts[letter] -= 1

        # Second pass for yellow and grey letters
        for i, letter in enumerate(guess):
            if result[i] == "":  # Only check letters not already marked green
                if answer_counts.get(letter, 0) > 0:
                    result[i] = "y"
                    answer_counts[letter] -= 1
                else:
                    result[i] = "x"

        return "".join(result)

    def filter_solution(self, guess: str, result: str) -> None:
        """
        Filters the solution list based on the guess and result.

        This works by checking if each potential solution word would have produced
        the same result if it were the answer. This is a robust way to handle
        all constraints, including those from duplicate letters.

        Args:
            guess: The guessed word.
            result: The result of the guess.
        """
        self.solution_space = [
            word
            for word in self.solution_space
            if WordleSolver.generate_result(guess, word) == result
        ]

    def get_best_guess(self) -> str | None:
        """
        Returns the best guess from the current solution space using a Minimax strategy.
        For the first guess, it returns a pre-calculated optimal word ('slate').
        For subsequent guesses, it finds the word from the *current solution space*
        that minimizes the size of the largest possible resulting solution space.
        This ensures that every guess is a potential answer (similar to "Hard Mode").
        """
        if not self.solution_space:
            return None

        # If only one or two solutions are left, just guess one of them.
        if len(self.solution_space) <= 2:
            return self.solution_space[0]

        # --- Performance Optimization for First Guess ---
        # The first guess is the most computationally expensive. By returning a
        # pre-calculated optimal starting word like 'slate', we avoid a long wait.
        # 'slate' is a widely recognized great starting word.
        if (
            len(self.solution_space) == len(self.full_dictionary)
            and "slate" in self.full_dictionary
        ):
            return "slate"

        best_guess = ""
        # The score of a guess is the size of the largest possible resulting
        # solution space. We want to minimize this "worst-case" outcome.
        best_score = float("inf")

        # The best guess is chosen from the remaining possible solutions.
        # This is equivalent to Wordle's "Hard Mode".
        possible_guesses = self.solution_space

        for guess in possible_guesses:
            # For each possible guess, see what partitions it would create
            # in the current solution space.
            partition_sizes: Counter[str] = Counter()
            for answer in self.solution_space:
                result = WordleSolver.generate_result(guess, answer)
                partition_sizes[result] += 1

            # The "score" of a guess is the size of the largest partition it creates.
            score = max(partition_sizes.values())

            # We are looking for the guess with the smallest worst-case partition.
            if score < best_score:
                best_score = score
                best_guess = guess

        return best_guess

    def solve(self, answer: str, max_guesses: int = 20) -> int:
        """
        Solves the Wordle puzzle for a given answer.

        Returns:
            The number of guesses taken to solve the puzzle.

        Raises:
            RuntimeError: If the solver exceeds max_guesses.
        """
        guesses = []
        while len(self.solution_space) != 1:
            guess = self.get_best_guess()
            if guess is None:
                raise RuntimeError("No solution found")
            guesses.append(guess)
            result = WordleSolver.generate_result(guess, answer)
            self.filter_solution(guess, result)
            if len(guesses) >= max_guesses:
                raise RuntimeError(
                    f"Solver exceeded {max_guesses} guesses for answer" f" '{answer}'"
                )
        return len(guesses)
