from IPython import get_ipython

from learn_python.framework._formatter import format_results
from learn_python.framework._queue import default_queue

_post_execute_hook_ref = None


def ipython_setup():
    global _post_execute_hook_ref

    ipython = get_ipython()

    if not ipython:
        print("IPython environment not detected. Skipping IPython setup.")
        return

    # Remove any existing hook first (in case cell is re-run)
    if _post_execute_hook_ref is not None:
        try:
            ipython.events.unregister("post_execute", _post_execute_hook_ref)
        except ValueError:
            pass

    # Register new hook and store reference
    ipython.events.register("post_execute", _post_execute_hook)
    _post_execute_hook_ref = _post_execute_hook


def _post_execute_hook():
    results = default_queue.run()
    format_results(results)
