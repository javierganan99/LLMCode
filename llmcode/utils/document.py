"""
This module provides functionality for documenting Python scripts.

It includes functions to parse Python scripts, extract classes and functions,
and generate or update docstrings using a completion model.

Functions:
    doc_element: Generates a docstring for a given element using a completion model.
    doc_python_file: Documents a Python file by generating or updating docstrings for its elements.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

import re
from threading import Event
import llmcode.cfg.custom_params as custom_params
from .file_utils import (
    extract_functions_and_classes_from_python_tokens,
    parse_python,
    read_content,
)
from .completion import run_with_timeout, get_completion
from . import ANSI_CODE
from .logger import LOGGER


def doc_element(element, prompt, get_completion):
    return run_with_timeout(
        get_completion,
        args=(
            read_content(prompt).replace(custom_params.query_completion_key, element),
        ),
        timeout=custom_params.completion_timeout,
    )


def doc_python_file(
    script,
    prompts,
    elements2doc=custom_params.elements2doc,
    overwrite=custom_params.overwrite,
    get_completion=get_completion,
    stop_flag=Event(),
    TODO_message="# TODO: Document this ELEMENT on your own. Could not be documented by the model.",
):
    script = str(script)
    try:
        parsed = parse_python(script)
        if parsed is None:
            LOGGER.info(
                "%s\r❌Check the script {script}. It is not properly coded and can not be documented.",
                ANSI_CODE["red"],
            )
            return None
        (
            classes_and_functions,
            script_content,
        ) = extract_functions_and_classes_from_python_tokens(parsed)
    except Exception as e:
        LOGGER.info(
            "%s\r❌Check the script %s. The following error occurred: %s",
            ANSI_CODE["red"],
            script,
            e,
        )

    def add_msg(msg, where, element, script_content):
        n_spaces = 0
        for ch in element[where - 1 :: -1]:
            if ch == " ":
                n_spaces += 1
            else:
                break
        new_element = element[:where] + msg + "\n" + " " * n_spaces + element[where:]
        return script_content.replace(element, new_element)

    for e_type, elements in classes_and_functions.items():
        for element, e_name, dosctring_idx in elements:
            if (
                elements2doc is not None and e_name not in elements2doc
            ):  # Filter the elements to document
                continue
            if stop_flag.is_set():
                LOGGER.info(
                    "%s\r Ended during the documentation of script %s. Interrupted by SIGINT.%s",
                    ANSI_CODE["yellow"],
                    script,
                    ANSI_CODE["reset"],
                )
                return
            if e_type == "function" or e_type == "class":
                if element[dosctring_idx : dosctring_idx + 3] == '"""':
                    previous_docstring = re.search(r'"""(.*?)"""', element, re.DOTALL)
                    if (
                        previous_docstring and not overwrite
                    ):  # If element had docstring and we do not want to change it
                        continue
                    LOGGER.info(
                        "%s\r\n🤖 Generating docstring for %s %s...\n\n",
                        ANSI_CODE["reset"],
                        e_type,
                        e_name,
                    )
                else:
                    previous_docstring = None
                result = doc_element(element, prompts[e_type], get_completion)
                if result is not None:  # Query successfull
                    new_docstring = re.search(r'"""(.*?)"""', result, re.DOTALL)
                    if new_docstring:
                        new_docstring = new_docstring.group(1)
                        LOGGER.info("%s\r%s\n\n\n", ANSI_CODE["reset"], new_docstring)
                    else:
                        LOGGER.info(
                            "%s\r⚠ No docstring generated for %s %s...",
                            ANSI_CODE["yellow"],
                            e_type,
                            e_name,
                        )
                        script_content = add_msg(
                            TODO_message.replace("ELEMENT", e_type),
                            dosctring_idx,
                            element,
                            script_content,
                        )
                        continue
                    if previous_docstring:  # If element had docstring
                        previous_docstring = previous_docstring.group(1)
                        element_new = element.replace(
                            previous_docstring, new_docstring, 1
                        )
                        script_content = script_content.replace(element, element_new, 1)
                    else:  # If element did not have docstring
                        script_content = add_msg(
                            f'"""{new_docstring}"""',
                            dosctring_idx,
                            element,
                            script_content,
                        )
                else:  # Error in the query
                    LOGGER.info(
                        "%s\r❌ Error in the query for %s %s! No response provided...",
                        ANSI_CODE["red"],
                        e_type,
                        e_name,
                    )
                    script_content = add_msg(
                        TODO_message.replace("ELEMENT", e_type),
                        dosctring_idx,
                        element,
                        script_content,
                    )
    with open(script, "w", encoding="utf-8") as python_file:
        python_file.write(script_content)
