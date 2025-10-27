from learn_python.framework._exercise import Exercise


def test_extra_solution_fixture():
    """Test that 'solution' parameter is handled correctly."""
    exercise = Exercise()

    def solution():
        # This fixture named 'solution' should be ignored
        return "This should not be injected"

    def test_edge(solution):
        # 'solution' here is the actual solution passed to run_tests
        assert solution == "actual_solution"
        return "Correct solution used"

    exercise._register_test(test_edge, "Edge case test")
    results = exercise.run_tests("actual_solution")

    assert len(results) == 1
    assert results[0].status == "success"


def test_solution_parameter_not_first():
    """Test that 'solution' parameter can be in any position."""
    exercise = Exercise()

    def data():
        return [2, 3]

    def test_solution_not_first(data, solution):
        assert solution(data) == 5
        return "Solution works"

    def add_solution(numbers):
        return sum(numbers)

    exercise._register_fixture(data, "data")
    exercise._register_test(test_solution_not_first, "Solution not first test")
    results = exercise.run_tests(add_solution)

    assert len(results) == 1
    assert results[0].status == "success"


def test_no_solution_parameter():
    """Test that tests without 'solution' parameter still run."""
    exercise = Exercise()

    def test_no_solution():
        assert 1 + 1 == 2
        return "Math works"

    exercise._register_test(test_no_solution, "No solution parameter test")
    results = exercise.run_tests(lambda: None)

    assert len(results) == 1
    assert results[0].status == "success"
