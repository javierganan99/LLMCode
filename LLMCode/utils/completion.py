import threading
import openai
import LLMCode.cfg.completion_params as completion_params
from . import ANSI_CODE
from .logger import LOGGER


def run_with_timeout(target_function, args=(), kwargs={}, timeout=30):
    result = [None]  # A mutable container to store the function result
    exception = [None]  # A container to capture exceptions

    def target_wrapper():
        try:
            result[0] = target_function(*args, **kwargs)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target_wrapper)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        LOGGER.info(
            "%s⚠ The completion could not be done. %s response lasted more than %s seconds, which is the limit.",
            ANSI_CODE["yellow"],
            target_function.__name__,
            timeout,
        )
        return None
    if exception[0]:
        LOGGER.info(
            "%s⚠ The completion could not be done. %s raised the exception %s",
            ANSI_CODE["yellow"],
            target_function.__name__,
            exception[0],
        )
        return None
    return result[0]


# Completion using openai API
def get_completion_openai(prompt):
    params = {
        key: value
        for key, value in vars(completion_params).items()
        if not key.startswith("__")
    }
    return (
        openai.ChatCompletion.create(
            messages=[{"role": "user", "content": prompt}], **params
        )
        .choices[0]
        .message.content
    )


# The completion function to use
get_completion = globals()[vars(completion_params).pop("completion_function")]
