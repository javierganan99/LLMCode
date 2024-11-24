import shutil
import os
import re
import inspect
from llmcode.utils import document
from llmcode.cfg.custom_params import document_prompts
from llmcode.utils.completion import get_completion_openai
from llmcode.utils import completion
from llmcode.utils.file_utils import read_content


def find_functions_in_module(module, match):
    matching_functions = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and match in name:
            matching_functions.append(obj)
    return matching_functions


def test_doc_element():
    my_function = """
    def sum(a,b):
        return a+b
    """
    my_class = """
    class Definition:
        NAME = "Rigoberto"
    """
    for completion_function in find_functions_in_module(completion, "get_completion"):
        result = document.doc_element(
            element=my_function,
            prompt=document_prompts["python"]["function"],
            get_completion=completion_function,
        )
        assert result is None or isinstance(result, str)
        result = document.doc_element(
            element=my_class,
            prompt=document_prompts["python"]["class"],
            get_completion=completion_function,
        )
        assert result is None or isinstance(result, str)


def test_doc_python_file(good_example_python_file):
    new_file = str(good_example_python_file).replace(
        good_example_python_file.stem,
        good_example_python_file.stem + "_toRemove",
    )
    shutil.copy(good_example_python_file, new_file)
    prev_content = read_content(new_file)
    test_message = " # TODO: Test message"
    document.doc_python_file(
        script=new_file,
        get_completion=get_completion_openai,
        prompts=document_prompts["python"],
        TODO_message=test_message,
    )
    new_content = read_content(new_file)
    matches = re.findall(r'(""".*?""")', new_content, re.DOTALL)
    assert len(matches) or test_message in new_content
    for match in matches:
        new_content = new_content.replace(match, "")
    new_content = new_content.replace(test_message, "")
    assert new_content.replace("\n", "").replace("\t", "").replace(
        " ", ""
    ) == prev_content.replace("\n", "").replace("\t", "").replace(" ", "")
    os.remove(new_file)
