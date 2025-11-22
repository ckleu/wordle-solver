import os
import sys
from unittest.mock import patch

import pytest

# Import from the new modules
from wordle_solver.cli import (
    benchmarking_solver,
    get_command_line_args,
    main,
    solve_wordle_puzzle,
)
from wordle_solver.solver import read_dictionary


@pytest.fixture
def full_dictionary():
    """
    pytest fixture to provide a controlled dictionary for testing.
    This creates a dummy dictionary file for testing purposes.
    """
    dummy_file_name = "dummy-dictionary.txt"
    # Create the file in the current directory (project root)
    with open(dummy_file_name, "w") as f:
        f.write("apple\n")
        f.write("baker\n")
        f.write("crane\n")
        f.write("drate\n")
        f.write("slate\n")
        f.write("treat\n")
        f.write("zzzzz\n")

    # Pass the absolute path so read_dictionary (which uses os.path.join)
    # treats it as an absolute path and ignores the relative prefix.
    dictionary = read_dictionary(os.path.abspath(dummy_file_name))

    os.remove(dummy_file_name)

    return dictionary


# --- Tests for get_command_line_args ---


def test_get_command_line_args_solve(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py", "--solve"])
    args = get_command_line_args()
    assert args.solve is True
    assert args.bench is False


def test_get_command_line_args_bench(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py", "--bench"])
    args = get_command_line_args()
    assert args.solve is False
    assert args.bench is True


def test_get_command_line_args_no_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py"])
    with pytest.raises(SystemExit):
        get_command_line_args()


# --- Tests for CLI functions ---


def test_solve_wordle_puzzle(full_dictionary, capsys):
    """
    Tests the interactive solver by simulating user input.
    This test will not hang because it provides enough input to solve the puzzle.
    """
    # The solver's best first guess for this dictionary is 'slate'.
    # The answer we're aiming for is 'treat'.
    # The result for guess 'slate' with answer 'treat' is 'xxyyy'.
    # This single guess reduces the solution space to just ['treat'],
    # solving the puzzle.
    with patch("builtins.input", side_effect=["slate", "xxyyy"]):
        guess_count = solve_wordle_puzzle(full_dictionary)

    captured = capsys.readouterr()
    # Check that the solver suggested a guess
    assert "Suggested guess:" in captured.out
    # Check that the puzzle was solved
    assert "Solution space size: 1" in captured.out
    assert "['treat']" in captured.out
    # The loop runs once (guess_count=1), and the function returns guess_count + 1
    assert guess_count == 2


def test_solve_wordle_puzzle_invalid_input(full_dictionary, capsys):
    """
    Tests the interactive solver handles invalid user input.
    """
    # Simulate user entering a short guess, then a valid one.
    # Then an invalid result, then a valid one that solves the puzzle.
    with patch("builtins.input", side_effect=["bad", "slate", "bad", "xxyyy"]):
        solve_wordle_puzzle(full_dictionary)

    captured = capsys.readouterr()
    assert "Error: Guess must be 5 letters long." in captured.err
    assert (
        "Error: Result must be 5 characters and only contain "
        "'g', 'y', or 'x'." in captured.err
    )


def test_benchmarking_solver(full_dictionary, capsys):
    """
    Tests the benchmarking function to ensure it runs and prints output.
    """
    benchmarking_solver(full_dictionary)
    captured = capsys.readouterr()
    assert "Average:" in captured.out
    assert "Guess Distribution:" in captured.out


def test_benchmarking_solver_with_failures(capsys):
    """
    Tests the benchmarking function handles solver failures.
    """
    # Mock the solve method to always raise a RuntimeError to simulate failure.
    with patch(
        "wordle_solver.solver.WordleSolver.solve",
        side_effect=RuntimeError("Solver failed"),
    ):
        benchmarking_solver(["words"])
        captured = capsys.readouterr()
        assert "No puzzles were solved successfully." in captured.out
        assert "Failed to solve" in captured.out


# --- Tests for main entry point ---


def test_main_dispatch_to_solve(monkeypatch):
    """
    Tests that main() calls solve_wordle_puzzle with the --solve argument.
    """
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py", "--solve"])
    # Mock the parts we don't want to actually run
    with patch("wordle_solver.cli.read_dictionary", return_value=["crane"]), patch(
        "wordle_solver.cli.solve_wordle_puzzle"
    ) as mock_solve:
        main()
        mock_solve.assert_called_once()


def test_main_dispatch_to_bench(monkeypatch):
    """
    Tests that main() calls benchmarking_solver with the --bench argument.
    """
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py", "--bench"])
    with patch("wordle_solver.cli.read_dictionary", return_value=["crane"]), patch(
        "wordle_solver.cli.benchmarking_solver"
    ) as mock_bench:
        main()
        mock_bench.assert_called_once()


def test_main_file_not_found(monkeypatch, capsys):
    """
    Tests that main() handles FileNotFoundError gracefully.
    """
    monkeypatch.setattr(sys, "argv", ["wordle_solver.py", "--solve"])
    with patch(
        "wordle_solver.cli.read_dictionary",
        side_effect=FileNotFoundError("dictionary.txt not found"),
    ):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1

    captured = capsys.readouterr()
    assert "Dictionary not found" in captured.err
