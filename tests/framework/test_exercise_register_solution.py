from learn_python.framework import Exercise, TestQueue, default_queue


def test_register_solution_with_custom_queue():
    """Test register_solution decorator with custom queue."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test addition")
    def test_add(solution):
        assert solution(2, 3) == 5
        return "Good math"

    @exercise.register_solution(queue)
    def my_solution(a, b):
        return a + b

    # Check it was added to the queue
    assert len(queue.queue) == 1
    assert queue.queue[0][0] is exercise
    assert queue.queue[0][1] is my_solution


def test_register_solution_with_default_queue():
    """Test register_solution decorator uses default_queue when no queue specified."""
    default_queue.clear()

    exercise = Exercise()

    @exercise.test("Test")
    def test_func(solution):
        assert solution() == 100
        return "Pass"

    @exercise.register_solution()
    def my_solution():
        return 100

    # Check it was added to default queue
    assert len(default_queue.queue) == 1
    assert default_queue.queue[0][0] is exercise
    assert default_queue.queue[0][1] is my_solution


def test_register_solution_decorator_returns_function():
    """Test that register_solution decorator returns the original function."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test")
    def test_func(solution):
        return "OK"

    @exercise.register_solution(queue)
    def my_solution():
        return 42

    # Function should still be callable
    assert my_solution() == 42


def test_register_solution_runs_successfully():
    """Test that registered solution can be run through queue."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test square")
    def test_square(solution):
        assert solution(5) == 25
        return "Correct"

    @exercise.register_solution(queue)
    def square(x):
        return x * x

    results = queue.run()

    assert len(results) == 1
    assert results[0].status == "success"
