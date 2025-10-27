from learn_python.framework import format_results, Exercise
from io import StringIO
import sys


def test_format_results_with_success():
    """Test formatting successful test results."""
    exercise = Exercise()

    @exercise.test("Test 1")
    def test_one(solution):
        assert solution() == 42
        return "Good job"

    results = exercise.run_tests(lambda: 42)

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    format_results(results)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "✓" in output
    assert "Test 1" in output
    assert "Good job" in output
    assert "All 1 tests passed!" in output


def test_format_results_with_failure():
    """Test formatting failed test results."""
    exercise = Exercise()

    @exercise.test("Test 1")
    def test_one(solution):
        assert solution() == 100, "Expected 100"
        return "Good"

    results = exercise.run_tests(lambda: 42)

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    format_results(results)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "✗" in output
    assert "Test 1" in output
    assert "0/1 tests passed" in output


def test_format_results_with_parametrized():
    """Test formatting parametrized test results."""
    exercise = Exercise()

    @exercise.parametrize("x,expected", [(2, 4), (3, 9), (4, 16)])
    @exercise.test("Square test")
    def test_square(solution, x, expected):
        assert solution(x) == expected
        return "Good"

    results = exercise.run_tests(lambda x: x * x)

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    format_results(results)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "✓" in output
    assert "Square test" in output
    assert "3/3 complete" in output


def test_format_results_mixed():
    """Test formatting mix of success and failure."""
    exercise = Exercise()

    @exercise.test("Pass test")
    def test_pass(solution):
        assert solution(1) == 1
        return "OK"

    @exercise.test("Fail test")
    def test_fail(solution):
        assert solution(2) == 999
        return "OK"

    results = exercise.run_tests(lambda x: x)

    # Capture output
    captured_output = StringIO()
    sys.stdout = captured_output

    format_results(results)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()

    assert "✓" in output  # Has success
    assert "✗" in output  # Has failure
    assert "1/2 tests passed" in output
