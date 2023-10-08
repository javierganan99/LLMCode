import pytest
from LLMCode.utils import file_utils
import tokenize
import os
import shutil
from pathlib import Path


def test_parse_python(good_example_python_file, bad_example_python_file):
    toks = file_utils.parse_python(good_example_python_file)
    assert isinstance(toks, list)
    for tok in toks:
        assert isinstance(tok, tokenize.TokenInfo)
        assert tok.type != 59  # Error token
    with pytest.raises(Exception) as exc_info:
        toks = file_utils.parse_python(bad_example_python_file)
    assert str(exc_info.value) == "Script could not be tokenized"


def test_extract_functions_and_classes_from_python_tokens(good_example_python_file):
    with open(good_example_python_file, "r") as file:
        orginal_content = file.read()
    tokens = file_utils.parse_python(good_example_python_file)
    stored, code = file_utils.extract_functions_and_classes_from_python_tokens(tokens)
    for k, v in stored.items():
        if k == "class":  # Assert all classes readed
            assert len(v) == 1
        elif k == "function":
            assert len(v) == 3  # Assert all functions readed
        for content, name, idx in v:  # Assert all values proper type
            assert (
                isinstance(content, str)
                and isinstance(name, str)
                and isinstance(idx, int)
            )
    assert code == orginal_content  # Assert original content not modified


def test_is_file_in_directory(good_example_python_file):
    assert file_utils.is_file_in_directory(
        Path(good_example_python_file).parent, Path(good_example_python_file).name
    )
    assert not file_utils.is_file_in_directory(
        Path(good_example_python_file).parent, "non_existing_file"
    )


def test_copy_path(good_example_python_file):
    # Check copied file
    formatted_path = file_utils.copy_path(
        good_example_python_file, add_to_parent="_toRemove"
    )
    os.remove(formatted_path)
    # Check file not copied because non existing file
    with pytest.raises(FileNotFoundError) as exc_info:
        path = Path(good_example_python_file).parent / "non_existing_file"
        file_utils.copy_path(path)
    assert str(exc_info.value) == f"\u001b[31m\r❌Error: '{path}' does not exist."
    # Check file not copied because not supported extension
    formatted_path = file_utils.copy_path(
        Path(good_example_python_file).with_suffix(".txt")
    )
    assert formatted_path is None
    # Check folder copied
    formatted_path = file_utils.copy_path(
        Path(good_example_python_file.parent), add_to_parent="_toRemove"
    )
    shutil.rmtree(formatted_path)


def test_ensure_folder_exist(good_example_python_file):
    assert file_utils.ensure_folder_exist(Path(good_example_python_file).parent)
    path = Path(good_example_python_file).parent.parent / "toRemoveFolder"
    assert not file_utils.ensure_folder_exist(path)
    shutil.rmtree(path)


def test_get_temp_folder():
    folder = file_utils.get_temp_folder()
    assert Path(folder).exists()
