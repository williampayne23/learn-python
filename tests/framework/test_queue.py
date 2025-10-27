from learn_python.framework import TestQueue, Exercise


def test_queue_run_single_exercise():
    """Test running a single exercise from queue."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test 1")
    def test_one(solution):
        assert solution() == 42
        return "Success"

    queue.add(exercise, lambda: 42)
    results = queue.run()

    assert len(results) == 1
    assert results[0].status == "success"
    assert results[0].test_name == "Test 1"


def test_queue_run_multiple_exercises():
    """Test running multiple exercises from queue."""
    queue = TestQueue()

    ex1 = Exercise()
    @ex1.test("Test A")
    def test_a(solution):
        assert solution() == 1
        return "Good"

    ex2 = Exercise()
    @ex2.test("Test B")
    def test_b(solution):
        assert solution() == 2
        return "Great"

    queue.add(ex1, lambda: 1)
    queue.add(ex2, lambda: 2)

    results = queue.run()

    assert len(results) == 2
    assert results[0].test_name == "Test A"
    assert results[1].test_name == "Test B"
    assert all(r.status == "success" for r in results)


def test_queue_add_returns_self():
    """Test that add returns self for chaining."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test")
    def test_func(solution):
        return "OK"

    result = queue.add(exercise, lambda: None)
    assert result is queue


def test_queue_run_clears_by_default():
    """Test that run() clears the queue by default."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test")
    def test_func(solution):
        return "OK"

    queue.add(exercise, lambda: None)
    queue.run(clear=True)

    assert len(queue.queue) == 0


def test_queue_run_no_clear():
    """Test that run(clear=False) preserves the queue."""
    queue = TestQueue()
    exercise = Exercise()

    @exercise.test("Test")
    def test_func(solution):
        return "OK"

    queue.add(exercise, lambda: None)
    queue.run(clear=False)

    assert len(queue.queue) == 1
