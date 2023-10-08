import openai
import LLMCode.cfg.completion_params as completion_params
import multiprocessing
from . import ANSI_CODE


def run_with_timeout(target_function, args=None, timeout=30):
    pool = multiprocessing.Pool(processes=1)
    if args is None:
        result = pool.apply_async(target_function)
    else:
        result = pool.apply_async(target_function, args)
    try:
        result_value = result.get(timeout=timeout)
        return result_value
    except multiprocessing.TimeoutError:
        print(
            f"{ANSI_CODE['yellow']}\r⚠ The completion could not be done. {target_function} response lasted more than {timeout} seconds, which is the limit."
        )
        pool.terminate()
        return None
    finally:
        pool.close()
        pool.join()


# Completion using openai API
def get_completion_openai(prompt):
    params = {
        key: value
        for key, value in vars(completion_params).items()
        if not key.startswith("__")
    }
    chat_completion = openai.ChatCompletion.create(
        messages=[{"role": "user", "content": prompt}], **params
    )
    return chat_completion.choices[0].message.content


# The completion function to use
get_completion = globals()[vars(completion_params).pop("completion_function")]
