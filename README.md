# Wordle Solver

A smart Python-based command-line tool that helps you solve Wordle puzzles efficiently. It can act as an interactive assistant or run benchmarks to evaluate its own strategy.

![Wordle Solver Demo](https://raw.githubusercontent.com/ContentAccess/public/main/wordle-solver/wordle-solver-demo.gif)

---

## 📜 Table of Contents

- [✨ Features](#-features)
- [💾 Installation](#-installation)
- [🚀 Usage](#-usage)
- [🧪 Development](#-development)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## ✨ Features

-   **Interactive Solver**: Get real-time suggestions for the optimal word to play next.
-   **"Hard Mode" Strategy**: Every guess is a valid potential solution based on the hints received, ensuring no wasted moves.
-   **Advanced Benchmarking**: Automatically play thousands of games to measure the solver's efficiency and see detailed performance statistics.
-   **Optimal First Guess**: Starts with **'slate'**, a pre-calculated optimal opening word, to maximize your chances from the very beginning.

---

## 💾 Installation

> **Note**: It is highly recommended to use a virtual environment to manage project dependencies.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/ckleu/wordle-solver.git
    cd wordle-solver
    ```

2.  **Create and Activate a Virtual Environment**:

    -   **macOS / Linux**:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
    -   **Windows**:
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```

3.  **Install the Project**:

    -   **For standard use**:
        ```bash
        pip install .
        ```
    -   **For development** (includes testing and linting tools):
        ```bash
        pip install -e .[test,dev]
        pre-commit install
        ```

---

## 🚀 Usage

Once installed, the `wordle-solver` command will be available in your terminal.

### Interactive Mode

To get real-time help with a puzzle, use the `--solve` flag. The solver will suggest a word. After you play it, provide the color results from Wordle.

-   `g` for **Green** (correct letter, correct position)
-   `y` for **Yellow** (correct letter, wrong position)
-   `x` for **Grey** (incorrect letter)

```bash
$ wordle-solver --solve

I suggest you play: slate
What was your guess: slate
What was your result (e.g., 'gyyxx'): xxyxg

Solution space size: 103
Suggested guess: crane
What was your guess: crane
What was your result (e.g., 'gyyxx'): ggyxx

Solution space size: 1
Solution space: ['craze']
The puzzle was solved in 3 guesses.
```

### Benchmarking Mode

To evaluate the solver's performance across thousands of simulated games, use the `--bench` flag.

```bash
$ wordle-solver --bench

Average: 3.68 guesses (max: 7) on 10000 successful solves.

Guess Distribution:
  Solved in 1 guesses: 1     (0.01%)
  Solved in 2 guesses: 244   (2.44%)
  Solved in 3 guesses: 2969  (29.69%)
  Solved in 4 guesses: 4648  (46.48%)
  Solved in 5 guesses: 1763  (17.63%)
  Solved in 6 guesses: 361   (3.61%)
  Solved in 7 guesses: 14    (0.14%)
```

---

## 🧪 Development

After installing the project for development (`pip install -e .[test,dev]`), you can use the following commands to run tests, format code, and perform static analysis.

-   **Run Tests**:
    ```bash
    pytest
    ```
-   **Check for Linting Errors**:
    ```bash
    ruff check .
    ```
-   **Format Code**:
    ```bash
    ruff format .
    black .
    ```
-   **Run Static Type Checking**:
    ```bash
    mypy src
    ```
-   **Run Pre-commit Hooks**:
    ```bash
    pre-commit run --all-files
    ```

## 🐧 WSL Support

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

---

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.