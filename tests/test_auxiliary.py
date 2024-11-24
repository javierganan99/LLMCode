import os
import pytest
from llmcode.utils import auxiliary
from llmcode.utils.auxiliary import _apply_to_scripts


def test_format_code(good_example_python_file):
    # Test Case 1: Good input
    result = auxiliary.format_code(
        good_example_python_file, exclude=[], languages=["python"]
    )
    assert result == True
    to_remove_file = str(good_example_python_file).replace(
        good_example_python_file.stem,
        good_example_python_file.stem + "_toRemove",
    )
    os.remove(to_remove_file)
    # Test Case 2: Programming language not supported
    result = auxiliary.format_code(good_example_python_file.with_suffix(".txt"))
    assert result == None
    # Test Case 3: Non existing file
    with pytest.raises(AssertionError) as exc_info:
        auxiliary.format_code("non_existing_file")
        assert "does not exist" in str(exc_info.value)
    # Test Case 4: Exclude folder that does not exists
    with pytest.raises(AssertionError) as exc_info:
        auxiliary.format_code(
            good_example_python_file.parent, exclude=["non_existing_folder"]
        )
        assert "Check the name of the file" in str(exc_info.value)


def simulated_function_to_execute(file, stop_flag, *args, **kwargs):
    pass


def test_apply_to_scripts():
    # Test Case 1: No files of provided extension in provided folder
    assert (
        _apply_to_scripts(
            f"tests{os.path.sep}test_material", "no_matter", ".cpp", "no_matter"
        )
        is None
    )
    # Test Case 2: Provided existing folder with files with proper extension
    assert _apply_to_scripts(
        f"tests{os.path.sep}test_material",
        simulated_function_to_execute,
        ".py",
        "no_matter",
    )
    # Test Case 3: Provided existing file with proper extension
    assert _apply_to_scripts(
        f"tests{os.path.sep}test_material{os.path.sep}good_python_example.py",
        simulated_function_to_execute,
        ".py",
        "no_matter",
    )
