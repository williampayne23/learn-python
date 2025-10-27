from learn_python.framework._exercise import Exercise
import pytest


def test_fixture_injection():
    """Test that fixtures are injected into test functions."""
    exercise = Exercise()

    def test_numbers():
        return [1, 2, 3, 4, 5]

    def test_sum(solution, test_numbers):
        result = solution(test_numbers)
        assert result == 15
        return "Sum is correct"

    def sum_solution(numbers):
        return sum(numbers)

    exercise._register_fixture(test_numbers, "test_numbers")
    exercise._register_test(test_sum, "Sum test")
    results = exercise.run_tests(sum_solution)

    assert len(results) == 1
    assert results[0].status == "success"


def test_multiple_fixtures():
    """Test that multiple fixtures can be injected."""
    exercise = Exercise()

    def numbers():
        return [1, 2, 3, 4, 5]

    def expected_sum():
        return 15

    def test_with_multiple(solution, numbers, expected_sum):
        result = solution(numbers)
        assert result == expected_sum
        return "Multiple fixtures work"

    def sum_solution(numbers):
        return sum(numbers)

    exercise._register_fixture(numbers, "numbers")
    exercise._register_fixture(expected_sum, "expected_sum")
    exercise._register_test(test_with_multiple, "Multiple fixtures test")
    results = exercise.run_tests(sum_solution)

    assert len(results) == 1
    assert results[0].status == "success"


def test_fixture_called_each_time():
    """Test that fixtures are called for each test execution."""
    exercise = Exercise()
    call_count = 0

    def counting_fixture():
        nonlocal call_count
        call_count += 1
        return call_count

    def test_one(solution, counting_fixture):
        assert counting_fixture == 1
        return "First call"

    def test_two(solution, counting_fixture):
        assert counting_fixture == 2
        return "Second call"

    def dummy_solution():
        return True

    exercise._register_fixture(counting_fixture, "counting_fixture")
    exercise._register_test(test_one, "Test one")
    exercise._register_test(test_two, "Test two")
    results = exercise.run_tests(dummy_solution)

    assert len(results) == 2
    assert results[0].status == "success"
    assert results[1].status == "success"
    assert call_count == 2


def test_fixture_overwritten_raises_error():
    """Test that defining a fixture with the same name raises an error."""
    exercise = Exercise()

    def duplicate_fixture():  # pyright: ignore[reportRedeclaration]
        return "First definition"

    exercise._register_fixture(duplicate_fixture, "duplicate_fixture")

    with pytest.raises(Exception) as excinfo:

        def duplicate_fixture():
            return "Second definition"

        exercise._register_fixture(duplicate_fixture, "duplicate_fixture")

    assert "with name 'duplicate_fixture' is already registered" in str(excinfo.value)
