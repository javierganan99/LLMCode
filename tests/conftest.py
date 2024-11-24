import os
from pathlib import Path
import pytest
from llmcode.utils import completion
from llmcode.cfg import custom_params


@pytest.fixture
def good_example_python_file():
    return Path(__file__).parent / os.path.sep.join(
        ["test_material", "good_python_example.py"]
    )


@pytest.fixture
def bad_example_python_file():
    return Path(__file__).parent / os.path.sep.join(
        ["test_material", "bad_python_example.txt"]
    )


@pytest.fixture
def mock_completion(mocker):
    return mocker.patch.object(
        completion,
        "get_completion",
        return_value='"""This is a custom docstring for the tests"""',
    )


@pytest.fixture(autouse=True)
def modify_custom_vars(monkeypatch):
    # Change the value of the 'rewrite' variable to True
    monkeypatch.setattr(custom_params, "rewrite", False)
    monkeypatch.setattr(custom_params, "surname", "_toRemove")
