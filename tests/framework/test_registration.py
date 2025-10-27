from learn_python.framework._exercise import Exercise


def test_test_decorator_registration():
    """Test that @exercise.test decorator registers tests."""
    exercise = Exercise()

    @exercise.test("Sample test")
    def test_func():
        return "Test passed"

    assert len(exercise.tests) == 1
    test_info = list(exercise.tests.values())[0]
    assert test_info.name == "Sample test"
    assert test_info.function == test_func


def test_test_decorator_default_name():
    """Test that @exercise.test uses function name when no name provided."""
    exercise = Exercise()

    @exercise.test()
    def my_custom_test():
        return "Test passed"

    assert len(exercise.tests) == 1
    test_info = list(exercise.tests.values())[0]
    assert test_info.name == "my_custom_test"
    assert test_info.function == my_custom_test


def test_fixture_decorator_registration():
    """Test that @exercise.fixture decorator registers fixtures."""
    exercise = Exercise()

    @exercise.fixture()
    def test_data():
        return [1, 2, 3, 4, 5]

    assert "test_data" in exercise.fixtures
    assert exercise.fixtures["test_data"]["function"] == test_data
    assert exercise.fixtures["test_data"]["name"] == "test_data"


def test_fixture_decorator_custom_name():
    """Test that @exercise.fixture can use custom names."""
    exercise = Exercise()

    @exercise.fixture("Custom Data")
    def test_data():
        return [1, 2, 3]

    assert "Custom Data" in exercise.fixtures
    assert exercise.fixtures["Custom Data"]["name"] == "Custom Data"
    assert exercise.fixtures["Custom Data"]["function"] == test_data
