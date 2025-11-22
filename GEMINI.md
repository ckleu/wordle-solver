# Gemini Project Context: Wordle Solver

This document provides specific instructions and context for the Wordle Solver project to facilitate effective interaction with Gemini.

## 1. Project Overview

The project is a Python-based command-line tool for solving Wordle puzzles. It offers two main functionalities:
1.  **Interactive Solver**: Provides real-time suggestions for the best word to guess next based on user feedback.
2.  **Benchmarking Tool**: Runs simulations to evaluate the solver's performance and efficiency.

The tool operates on a "Hard Mode" strategy, meaning every guess is a valid potential solution based on the hints received so far.

## 2. Core Logic: The `WordleSolver` Class

The heart of the application is the `WordleSolver` class in `src/wordle_solver/solver.py`.

-   **Initialization**: The solver is initialized with a complete dictionary of valid five-letter words. This forms the initial "solution space."
-   **Filtering (`filter_solution`)**: After each guess, the `solution_space` is pruned. The method works by iterating through all remaining possible solutions and keeping only those that would have produced the *exact same feedback* (e.g., 'gyyxx') if they were the correct answer.
-   **Guessing Strategy (`get_best_guess`)**:
    -   **First Guess**: For performance, the solver returns the pre-calculated optimal starting word: **'slate'**.
    -   **Subsequent Guesses**: The solver uses a minimax strategy. It iterates through the remaining `solution_space` (as it's playing in "Hard Mode") and for each word, it calculates the "worst-case" outcome. The worst-case is the largest possible number of remaining solutions after that guess. The word that *minimizes* this worst-case scenario is chosen as the best guess.

## 3. Key Files

-   `pyproject.toml`: Defines project metadata, dependencies, and tool configurations (ruff, black, mypy, pytest).
-   `README.md`: Provides user-facing instructions for installation and usage.
-   `src/wordle_solver/cli.py`: Handles command-line argument parsing (`--solve`, `--bench`) and manages the user interaction loop and benchmarking process.
-   `src/wordle_solver/solver.py`: Contains the core `WordleSolver` class and the logic for reading the dictionary.
-   `english-usa-dictionary.txt`: The default dictionary file containing a list of five-letter English words.
-   `tests/`: Contains unit tests for the solver and CLI.

## 4. Development Setup

The project uses `venv` for environment management and `pip` for installation. **All commands must be run within the virtual environment.**

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
2.  **Install for development:**
    This command installs the project in editable mode (`-e`) and includes all testing and development dependencies.
    ```bash
    .\.venv\Scripts\python -m pip install -e .[test,dev]
    ```

## 5. Running the Application

The entry point is defined in `pyproject.toml` as `wordle-solver`.

-   **Interactive Mode**:
    ```bash
    wordle-solver --solve
    ```
-   **Benchmark Mode**:
    ```bash
    wordle-solver --bench
    ```

## 6. Testing and Linting

The project is configured with `pytest`, `ruff`, `black`, and `mypy`. **Always use the virtual environment's Python executable.**

-   **Run Tests**:
    ```bash
    .\.venv\Scripts\python -m pytest
    ```
-   **Check for Linting Errors**:
    ```bash
    .\.venv\Scripts\python -m ruff check .
    ```
-   **Format Code**:
    ```bash
    .\.venv\Scripts\python -m ruff format .
    .\.venv\Scripts\python -m black .
    ```
-   **Run Static Type Checking**:
    ```bash
    .\.venv\Scripts\python -m mypy src
    ```

## 7. Dependencies

-   **Production**: No external production dependencies are listed in `pyproject.toml`. The application relies only on the Python standard library.
-   **Development (`test`, `dev`)**:
    -   `pytest`: For running tests.
    -   `pytest-cov`: For measuring test coverage.
    -   `ruff`: For linting and formatting.
    -   `black`: For code formatting.
    -   `mypy`: For static type checking.

## 8. WSL Support

You can run the project within the Windows Subsystem for Linux (WSL). This is useful for verifying cross-platform compatibility.

1.  **Create a Linux virtual environment:**
    ```bash
    wsl python3 -m venv .venv-linux
    ```
2.  **Install dependencies:**
    ```bash
    wsl .venv-linux/bin/pip install -e .[test,dev]
    ```
3.  **Run Tests:**
    ```bash
    wsl .venv-linux/bin/pytest
    ```