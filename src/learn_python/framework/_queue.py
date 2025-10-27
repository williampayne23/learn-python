class TestQueue:
    """Queue for managing and running multiple exercises."""

    def __init__(self):
        self.queue = []

    def add(self, exercise, solution):
        """Add an exercise + solution to the queue.

        Args:
            exercise: Exercise instance to run
            solution: Solution function to test

        Returns:
            self for chaining
        """
        self.queue.append((exercise, solution))
        return self

    def run(self, clear=True):
        """Run all queued exercises and return results.

        Args:
            clear: Whether to clear the queue after running (default: True)

        Returns:
            List of all results from all exercises
        """
        all_results = []

        for exercise, solution in self.queue:
            results = exercise.run_tests(solution)
            all_results.extend(results)

        if clear:
            self.clear()

        return all_results

    def clear(self):
        """Clear the queue of pending exercises."""
        self.queue = []


# Global singleton queue instance
default_queue = TestQueue()
