import sys
from io import StringIO


class CaptureResult:
    """Result of capturing stdout/stderr."""
    def __init__(self, out, err):
        self.out = out
        self.err = err


class CaptureOutput:
    """Context manager for capturing stdout and stderr output."""

    def __init__(self):
        self._old_stdout = None
        self._old_stderr = None
        self._capture_stdout = None
        self._capture_stderr = None

    def __enter__(self):
        self._old_stdout = sys.stdout
        self._old_stderr = sys.stderr
        self._capture_stdout = StringIO()
        self._capture_stderr = StringIO()
        sys.stdout = self._capture_stdout
        sys.stderr = self._capture_stderr
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr
        return False

    def readouterr(self):
        """Read and return captured output, then clear the buffers."""
        out = self._capture_stdout.getvalue()
        err = self._capture_stderr.getvalue()

        # Clear buffers for next capture
        self._capture_stdout.truncate(0)
        self._capture_stdout.seek(0)
        self._capture_stderr.truncate(0)
        self._capture_stderr.seek(0)

        return CaptureResult(out, err)


def capture_output():
    """Create a context manager for capturing output.

    Usage:
        with capture_output() as captured:
            print("Hello")
            output = captured.readouterr()
            assert output.out == "Hello\\n"
    """
    return CaptureOutput()
