import time
from llmcode.utils import completion


def example_function(sleep_time):
    time.sleep(sleep_time)
    return True


def test_run_with_timeout():
    assert completion.run_with_timeout(
        example_function, args=(0.1,), timeout=10
    )  # Run it time
    assert (
        completion.run_with_timeout(example_function, args=(0.1,), timeout=0.05) is None
    )  # Not run in time
