import pytest
from learn_python.framework._exercise import all_exercises, Exercise

import learn_python.exercises  # noqa: F401 Imported to register to all_exercises


@pytest.mark.parametrize("exercise", all_exercises)
def test_all_exercises(exercise: Exercise):
    """Test that all exercises have at least one test registered."""

    assert len(exercise.tests) > 0, f"Exercise {exercise} has no tests registered"
    assert exercise.example_solution is not None, (
        f"Exercise {exercise} has no example solution defined"
    )
    results = exercise.run_tests(exercise.example_solution)

    assert all(result.status == "success" for result in results), (
        f"Example solution for exercise {exercise} does not pass all tests"
    )
