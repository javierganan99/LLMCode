"""
This module handles the completion functionality using an LLM API.

It provides functions to execute tasks with a timeout and to obtain completions
from LLM APIs based on specified parameters.

Functions:
    run_with_timeout: Executes a function with a specified timeout.
    get_completion_openai: Retrieves a completion from the OpenAI API using a prompt.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

import threading
import openai
import llmcode.cfg.completion_params as completion_params
from . import ANSI_CODE
from .logger import LOGGER


def run_with_timeout(target_function, args=(), kwargs={}, timeout=30):
    """
    Runs a target function with specified arguments and keyword arguments within a given timeout.

    This function uses a separate thread to execute the target_function with the provided args and kwargs.
    If the function completes within the timeout period, its result is returned. If it exceeds the timeout,
    or if an exception occurs during execution, the function will log an informative message and return None.

    Args:
        target_function (callable): The function to execute.
        args (tuple, optional): Positional arguments to pass to the target_function (default is empty tuple).
        kwargs (dict, optional): Keyword arguments to pass to the target_function (default is empty dictionary).
        timeout (int, optional): The time in seconds to wait for the function execution before timing out (default is 30).

    Returns:
        (any | None): The result of the target_function if it completes successfully; None if it times out or raises an exception.
    """
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
    """
    Generates a completion response from OpenAI's Chat API based on the provided prompt.

    This function takes a user-defined prompt and sends it to the OpenAI completion model,
    returning the content of the model's response. Additional parameters for the completion
    can be passed using the `completion_params` object, which is filtered to exclude any
    private attributes.

    Args:
        prompt (str): The input text that the model will generate a response for.

    Returns:
        (str): The content of the model's response.
    """
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
