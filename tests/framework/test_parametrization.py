from learn_python.framework._exercise import Exercise


def test_parametrization_registration():
    """Test that parametrization data can be stored on a test."""
    exercise = Exercise()

    def test_parametrized(solution, input_value, expected_output):
        result = solution(input_value)
        assert result == expected_output
        return "Parametrized test passed"

    test_cases = [
        (2, 4),
        (3, 9),
        (4, 16),
    ]

    exercise._register_test(test_parametrized, "Parametrized test")
    exercise._register_parametrization(
        test_parametrized._test_id,
        ("input_value", "expected_output"),
        [(input_value, expected_output) for input_value, expected_output in test_cases],
    )

    # Verify parametrization data is stored correctly
    test_info = exercise.tests[test_parametrized._test_id]
    assert test_info.param_data is not None
    assert test_info.param_data.argnames == ("input_value", "expected_output")
    assert test_info.param_data.argvalues == test_cases


def test_parametrization_execution():
    """Test that parametrized tests execute correctly."""
    exercise = Exercise()

    def test_parametrized(solution, input_value, expected_output):
        result = solution(input_value)
        assert result == expected_output
        return "Parametrized test passed"

    def square_solution(x):
        return x * x

    test_cases = [
        (2, 4),
        (3, 9),
        (4, 16),
    ]

    exercise._register_test(test_parametrized, "Parametrized test")
    exercise._register_parametrization(
        test_parametrized._test_id,
        ("input_value", "expected_output"),
        test_cases,
    )

    # Run the tests
    results = exercise.run_tests(square_solution)
    assert len(results) == 1  # One ParametrizedResult

    param_result = results[0]
    assert param_result.test_name == "Parametrized test"
    assert param_result.status == "success"
    assert param_result.score == 1.0
    assert len(param_result.results) == 3

    # Check individual results
    for individual_result in param_result.results:
        assert individual_result.status == "success"
