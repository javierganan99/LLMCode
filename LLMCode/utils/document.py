from .file_utils import (
    extract_functions_and_classes_from_python_tokens,
    parse_python,
    read_content,
)
from .completion import run_with_timeout, get_completion
import re
import LLMCode.cfg.custom_params as custom_params
from . import ANSI_CODE
from threading import Event


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
    TODO_message=f"# TODO: Document this ELEMENT on your own. Could not be documented by the model.",
):
    script = str(script)
    try:
        parsed = parse_python(script)
        if parsed is None:
            print(
                f"{ANSI_CODE['red']}\r❌Check the script {script}. It is not properly encoded and can not be documented."
            )
            return None
        (
            classes_and_functions,
            script_content,
        ) = extract_functions_and_classes_from_python_tokens(parsed)
    except Exception as e:
        print(
            f"{ANSI_CODE['red']}\r❌Check the script {script}. The following error occurred: {e}"
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
                print(
                    f"{ANSI_CODE['yellow']}\r Ended during the documentation of script {script}. Interrupted by SIGINT.{ANSI_CODE['reset']}"
                )
                return
            if e_type == "function" or e_type == "class":
                if element[dosctring_idx : dosctring_idx + 3] == '"""':
                    previous_docstring = re.search(r'"""(.*?)"""', element, re.DOTALL)
                    if (
                        previous_docstring and not overwrite
                    ):  # If element had docstring and we do not want to change it
                        continue
                    print(
                        f"{ANSI_CODE['reset']}\r\n🤖 Generating docstring for {e_type} {e_name}...\n\n"
                    )
                else:
                    previous_docstring = None
                result = doc_element(element, prompts[e_type], get_completion)
                if result is not None:  # Query successfull
                    new_docstring = re.search(r'"""(.*?)"""', result, re.DOTALL)
                    if new_docstring:
                        new_docstring = new_docstring.group(1)
                        print(f"{ANSI_CODE['reset']}\r{new_docstring}\n\n\n")
                    else:
                        print(
                            f"{ANSI_CODE['yellow']}\r⚠ No docstring generated for {e_type} {e_name}..."
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
                    print(
                        f"{ANSI_CODE['red']}\r❌ Error in the query for {e_type} {e_name}! No response provided..."
                    )
                    script_content = add_msg(
                        TODO_message.replace("ELEMENT", e_type),
                        dosctring_idx,
                        element,
                        script_content,
                    )
                    pass
    with open(script, "w") as python_file:
        python_file.write(script_content)
