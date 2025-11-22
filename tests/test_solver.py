import pytest

from wordle_solver.solver import WordleSolver, read_dictionary


@pytest.fixture
def simple_dictionary():
    """A pytest fixture for a simple word list."""
    return ["apple", "baker", "crane", "drate", "slate", "treat", "zzzzz"]


@pytest.fixture
def solver_instance(simple_dictionary):
    """A pytest fixture for a WordleSolver instance."""
    return WordleSolver(simple_dictionary)


def test_read_dictionary_file_not_found():
    """
    Tests that read_dictionary raises FileNotFoundError for a missing file.
    """
    with pytest.raises(FileNotFoundError):
        read_dictionary("non_existent_file.txt")


# --- Tests for generate_result ---


def test_generate_result_all_correct():
    """
    Tests the generate_result method with a correct guess.
    """
    assert WordleSolver.generate_result("apple", "apple") == "ggggg"


def test_generate_result_all_incorrect():
    """
    Tests the generate_result method with all incorrect letters.
    """
    assert WordleSolver.generate_result("xyzzy", "apple") == "xxxxx"


def test_generate_result_mixed():
    """
    Tests the generate_result method with a mix of correct, misplaced, and incorrect
    letters.
    """
    # guess: crane, answer: treat -> xgyxy
    # c: wrong, r: right spot, a: wrong spot, n: wrong, e: wrong spot
    assert WordleSolver.generate_result("crane", "treat") == "xgyxy"
    # guess: slate, answer: treat -> xxyyy
    # s: wrong, l: wrong, a: wrong spot, t: wrong spot, e: wrong spot
    assert WordleSolver.generate_result("slate", "treat") == "xxyyy"
    # guess: apple, answer: treat -> yxxxy
    # a: wrong spot, p: wrong, p: wrong, l: wrong, e: wrong spot
    assert WordleSolver.generate_result("apple", "treat") == "yxxxy"


def test_generate_result_with_duplicates():
    """
    Tests generate_result with duplicate letters in the guess and answer.
    """
    # guess: teeth, answer: treat -> gxgyx
    # t: right spot, e: wrong, e: right spot, t: wrong spot, h: wrong
    assert WordleSolver.generate_result("teeth", "treat") == "gxgyx"
    # guess: apple, answer: paper -> yygxy
    # a: wrong spot, p: right spot, p: wrong spot, l: wrong, e: wrong spot
    assert WordleSolver.generate_result("apple", "paper") == "yygxy"


# --- Tests for filter_solution ---


def test_filter_solution(solver_instance):
    """
    Tests that filter_solution correctly reduces the solution space.
    """
    solver_instance.filter_solution("slate", "xxyyy")
    # The only word in simple_dictionary that gives "xxyyy" for "slate" is "treat"
    assert solver_instance.solution_space == ["treat"]


# --- Tests for get_best_guess ---


def test_get_best_guess_first_guess(solver_instance):
    """
    Tests that get_best_guess returns the optimal starting word ('slate').
    """
    assert solver_instance.get_best_guess() == "slate"


def test_get_best_guess_small_solution_space(solver_instance):
    """
    Tests get_best_guess when the solution space is small (<= 2 words).
    """
    solver_instance.solution_space = ["apple", "baker"]
    assert solver_instance.get_best_guess() in ["apple", "baker"]
    solver_instance.solution_space = ["treat"]
    assert solver_instance.get_best_guess() == "treat"


def test_get_best_guess_no_solution(solver_instance):
    """
    Tests get_best_guess when the solution space is empty.
    """
    solver_instance.solution_space = []
    assert solver_instance.get_best_guess() is None


def test_get_best_guess_minimax(solver_instance):
    """
    Tests the minimax logic of get_best_guess.
    """
    # After guessing 'slate' and getting 'xxyyy', the space is ['treat'].
    # The next guess should be 'treat'.
    solver_instance.filter_solution("slate", "xxyyy")
    assert solver_instance.get_best_guess() == "treat"


# --- Tests for solve ---


def test_solve_success(simple_dictionary):
    """
    Tests the solve method for a successful run.
    """
    # Use a new solver instance to ensure a clean state
    solver = WordleSolver(simple_dictionary)
    # The solver should find 'treat' in 1 guess ('slate'), which narrows the
    # solution space to just ['treat']. The solve method returns the number of
    # guesses required to uniquely identify the solution.
    assert solver.solve("treat") == 1


def test_solve_failure(simple_dictionary):
    """
    Tests that the solve method raises an error if it exceeds max_guesses.
    """
    solver = WordleSolver(simple_dictionary)
    with pytest.raises(RuntimeError, match="Solver exceeded 1 guesses"):
        # Force a situation where it can't solve in one guess.
        solver.solve("zzzzz", max_guesses=1)
