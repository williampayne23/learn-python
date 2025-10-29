from collections.abc import Callable
from typing import Literal, Optional, Any
from pydantic import BaseModel
import inspect
import uuid


class Result(BaseModel):
    test_name: str
    status: Literal["success", "failure"]
    message: str


class ParametrizedResult(Result):
    results: list[Result]
    score: float  # Proportion of tests that passed (0.0 to 1.0)


class ParametrizeData(BaseModel):
    argnames: tuple[str, ...]
    argvalues: list[tuple[Any, ...]]


class TestFunction(BaseModel):
    name: str
    function: Callable
    param_data: Optional[ParametrizeData] = None


class Exercise:
    def __init__(self, name: Optional[str] = None):
        self.name = name or ""
        self.tests = {}  # UUID -> TestFunction
        self.fixtures = {}

    def test(self, name=None):
        def decorator(func):
            self._register_test(func, name)
            return func

        return decorator

    def fixture(self, name=None):
        def decorator(func):
            self._register_fixture(func, name)
            return func

        return decorator

    def score(self, queue=None):
        """Decorator to register a solution for this exercise to a queue.

        Usage:
            @exercise.register_solution()
            def my_solution():
                pass

        Args:
            queue: TestQueue to add to (defaults to global default_queue)

        Returns:
            Decorator function
        """

        def decorator(solution):
            from ._queue import default_queue

            target_queue = queue or default_queue
            target_queue.add(self, solution)
            return solution

        return decorator

    def parametrize(self, argnames, argvalues):
        """Parametrize a test with multiple sets of arguments.

        Args:
            argnames: Comma-separated string of argument names (e.g., "a,b,expected")
                      or a tuple of argument names
            argvalues: List of tuples, where each tuple contains values for the arguments
        """

        def decorator(func):
            if not hasattr(func, "_test_id"):
                raise ValueError(
                    f"Function {func.__name__} must be decorated with @exercise.test() "
                    "before using @exercise.parametrize()"
                )

            # Parse argnames if it's a string
            if isinstance(argnames, str):
                parsed_argnames = tuple(name.strip() for name in argnames.split(","))
            else:
                parsed_argnames = tuple(argnames)

            self._register_parametrization(func._test_id, parsed_argnames, argvalues)
            return func

        return decorator

    def run_tests(self, solution):
        results = []
        for test_info in self.tests.values():
            kwargs = self._get_kwargs_from_fixtures(test_info.function, solution)
            if test_info.param_data is not None:
                # Handle parametrized test
                result = self._run_parametrized_test(
                    test_info.function,
                    test_info.name,
                    test_info.param_data,
                    kwargs,
                )
                results.append(result)
            else:
                # Handle regular test
                result = self._run_single_test(
                    test_info.function,
                    test_info.name,
                    kwargs,
                )
                results.append(result)
        return results

    def _register_test(self, func, name=None):
        """Register a test function with an optional name."""
        test_id = str(uuid.uuid4())
        func._test_id = test_id
        self.tests[test_id] = TestFunction(
            name=name or func.__name__,
            function=func,
        )

    def _register_fixture(self, func, name=None):
        """Register a fixture function with an optional name."""
        key = name or func.__name__
        if key in self.fixtures:
            raise ValueError(f"Fixture with name '{key}' is already registered.")
        self.fixtures[key] = {
            "function": func,
            "name": key,
        }

    def _register_parametrization(self, test_id, argnames, argvalues):
        """Register parameterization for a specific test.

        Args:
            test_id: UUID of the test function
            argnames: Tuple of argument names
            argvalues: List of tuples with argument values
        """
        if test_id not in self.tests:
            raise ValueError(f"Test with id {test_id} not found")

        if self.tests[test_id].param_data is not None:
            raise ValueError(
                f"Test '{self.tests[test_id].name}' is already parametrized"
            )

        self.tests[test_id].param_data = ParametrizeData(
            argnames=argnames, argvalues=argvalues
        )

    def _get_kwargs_from_fixtures(self, func, solution) -> dict:
        """Get keyword arguments from fixtures based on function signature."""
        kwargs = {}

        # Get the function's parameters
        sig = inspect.signature(func)

        # Iterate through parameters (skip 'solution' which is passed separately)
        for param_name, param in sig.parameters.items():
            if param_name == "solution":
                kwargs[param_name] = solution
                continue
            # Check if a fixture with this name exists
            if param_name in self.fixtures:
                fixture_info = self.fixtures[param_name]
                fixture_func = fixture_info["function"]
                # Call the fixture function to get its value
                kwargs[param_name] = fixture_func()

        return kwargs

    def _run_parametrized_test(self, test_func, test_name, param_data, kwargs):
        """Run a parametrized test with multiple parameter sets."""

        individual_results = []

        # Run test for each parameter set
        for param_values in param_data.argvalues:
            # Create name for this parameter set
            param_str = "-".join(str(v) for v in param_values)
            individual_test_name = f"{test_name}[{param_str}]"
            extra_kwargs = {}
            for arg_name, arg_value in zip(param_data.argnames, param_values):
                extra_kwargs[arg_name] = arg_value

            individual_results.append(
                self._run_single_test(
                    test_func,
                    individual_test_name,
                    {**kwargs, **extra_kwargs},
                )
            )

        # Calculate score and overall status
        passed_count = sum(1 for r in individual_results if r.status == "success")
        total_count = len(individual_results)
        score = passed_count / total_count if total_count > 0 else 0.0
        overall_status = "success" if passed_count == total_count else "failure"

        summary_message = f"{passed_count}/{total_count} parameter sets passed"

        return ParametrizedResult(
            test_name=test_name,
            status=overall_status,
            message=summary_message,
            results=individual_results,
            score=score,
        )

    def _run_single_test(self, test_func, test_name, kwargs):
        """Run a single non-parametrized test."""
        try:
            success_message = test_func(**kwargs)
            return Result(
                test_name=test_name, status="success", message=success_message
            )
        except AssertionError as e:
            return Result(test_name=test_name, status="failure", message=str(e))
