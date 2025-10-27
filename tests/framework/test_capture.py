from learn_python.framework import capture_output


def test_capture_stdout():
    """Test that capture_output captures stdout."""
    with capture_output() as captured:
        print("Hello World")
        output = captured.readouterr()

    assert output.out == "Hello World\n"
    assert output.err == ""


def test_capture_stderr():
    """Test that capture_output captures stderr."""
    import sys

    with capture_output() as captured:
        print("Error message", file=sys.stderr)
        output = captured.readouterr()

    assert output.out == ""
    assert output.err == "Error message\n"


def test_capture_both():
    """Test that capture_output captures both stdout and stderr."""
    import sys

    with capture_output() as captured:
        print("Standard output")
        print("Error output", file=sys.stderr)
        output = captured.readouterr()

    assert output.out == "Standard output\n"
    assert output.err == "Error output\n"


def test_capture_multiple_reads():
    """Test that readouterr can be called multiple times."""
    with capture_output() as captured:
        print("First")
        first = captured.readouterr()

        print("Second")
        second = captured.readouterr()

    assert first.out == "First\n"
    assert second.out == "Second\n"


def test_capture_restores_stdout():
    """Test that stdout is restored after context exit."""
    import sys

    original_stdout = sys.stdout

    with capture_output() as captured:
        print("Captured")

    assert sys.stdout is original_stdout
