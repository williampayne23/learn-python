from learn_python.framework._exercise import Exercise


def test_run_tests_success():
    """Test that successful tests return success results."""
    exercise = Exercise()

    def test_add(solution):
        result = solution(2, 3)
        assert result == 5
        return "Addition works correctly"

    def add_solution(a, b):
        return a + b

    exercise._register_test(test_add, "Add numbers test")
    results = exercise.run_tests(add_solution)

    assert len(results) == 1
    assert results[0].test_name == "Add numbers test"
    assert results[0].status == "success"
    assert results[0].message == "Addition works correctly"


def test_run_tests_failure():
    """Test that failed assertions return failure results."""
    exercise = Exercise()

    def test_fail(solution):
        result = solution(2, 3)
        assert result == 10, "Expected 10 but got a different result"
        return "This should not be returned"

    def add_solution(a, b):
        return a + b

    exercise._register_test(test_fail, "Should fail")
    results = exercise.run_tests(add_solution)

    assert len(results) == 1
    assert results[0].test_name == "Should fail"
    assert results[0].status == "failure"
    assert "Expected 10" in results[0].message


def test_run_multiple_tests():
    """Test running multiple tests in sequence."""
    exercise = Exercise()

    def test_one(solution):
        assert solution(1, 1) == 2
        return "Test 1 passed"

    def test_two(solution):
        assert solution(5, 5) == 10
        return "Test 2 passed"

    def test_three(solution):
        assert solution(2, 2) == 100, "This should fail"
        return "Test 3 passed"

    def add_solution(a, b):
        return a + b

    exercise._register_test(test_one, "Test One")
    exercise._register_test(test_two, "Test Two")
    exercise._register_test(test_three, "Test Three")
    results = exercise.run_tests(add_solution)

    assert len(results) == 3
    assert results[0].status == "success"
    assert results[1].status == "success"
    assert results[2].status == "failure"
