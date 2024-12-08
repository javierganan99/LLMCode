"""
This module provides utility functions for file operations and code parsing.

It includes functions to parse Python scripts, extract functions and classes,
manage file and directory operations, and handle git submodules.

Functions:
    parse_python: Parses a Python file and returns its tokens.
    extract_functions_and_classes_from_python_tokens: Extracts functions and
        classes from Python tokens.
    read_content: Reads the content of a file.
    list_submodule_directories: Lists git submodule directories in a project.
    is_file_in_directory: Checks if a file or directory exists within a given directory.
    copy_path: Copies a file or directory to a new location with a modified name.
    ensure_folder_exist: Ensures that a folder exists, creating it if necessary.
    get_temp_folder: Returns the path to the system's temporary folder.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

import shutil
import subprocess
from tokenize import tokenize
from token import tok_name
import os
import platform
from pathlib import Path
from . import ANSI_CODE, SUFFIX
from .logger import LOGGER


def parse_python(fn):
    """
    Parses a Python script and returns its tokens.

    This function opens a Python script file, reads its content, and tokenizes it using
    the tokenize module. It checks for any errors in the script and raises an exception
    if any error tokens are found. The function ensures that the file is closed properly
    after reading.

    Args:
        fn (str): The path to the Python script file to be parsed.

    Returns:
        (list): A list of tokens parsed from the script.
    """
    fp = open(fn, mode="rb")
    try:
        toks = list(tokenize(fp.readline))
        for tok in toks:
            if tok_name[tok.type] == "ERRORTOKEN":
                raise ValueError(
                    f"{ANSI_CODE['red']}\r❌ Check the script {fn}. It contains errors."
                )
    except Exception as e:
        raise ValueError("Script could not be tokenized") from e
    finally:
        fp.close()
    toks.pop(0)
    return toks


def extract_functions_and_classes_from_python_tokens(tokens):
    """
    Extract functions and classes from tokenized Python code.

    This function processes a list of tokens representing a Python script and extracts
    the definitions of functions and classes along with their associated docstrings.
    It handles indentation levels to accurately determine the boundaries of each
    extracted element.

    Args:
        tokens (list of tuple): A list of tokenized elements, where each element is a
                                tuple containing the token type and additional
                                information.

    Returns:
        (tuple): A tuple containing two elements:
            - (dict): A dictionary with keys "class" and "function", each mapping to a
                      list of tuples containing the source code of the functions or
                      classes and their names, as well as the position of their
                      docstrings.
            - (str): The reconstructed Python code as a string.
    """
    python_code = ""  # To store the code of the original Python file
    current_row = 0
    current_column = 0
    current_idx = {"class": "", "function": ""}
    stored = {"class": [], "function": []}
    reading = {"class": False, "function": False}
    indents = {"class": 0, "function": 0}
    dedents = {"class": 0, "function": 0}
    docstring_pos = {"class": None, "function": None}
    name = {"class": None, "function": None}
    prev_token = None
    # Read the tokenized script from the input file
    for token_line in tokens:
        tt, ts, rc0, rc1, _ = token_line
        ttn = tok_name[tt].lower()
        start_row, end_row, start_col, end_col, token_type, token = (
            int(rc0[0]),
            int(rc1[0]),
            int(rc0[1]),
            int(rc1[1]),
            ttn,
            ts,
        )
        if token_type in ["newline", "nl"]:
            token = "\n"
        elif token_type == "indent":
            col_diff = end_col - start_col
            token = " " * col_diff
            for k, v in reading.items():
                if v:
                    if indents[k] == 0 and dedents[k] == 0:
                        docstring_pos[k] = len(python_code) + col_diff - current_idx[k]
                    indents[k] += 1
        elif token_type == "dedent":
            for k, v in reading.items():
                if v:
                    dedents[k] += 1
        # Reset the column idx
        if current_row < start_row:
            current_column = 0
        # Ensure the current column matches the token's starting column
        while current_column < start_col:
            python_code += " "  # Add spaces for missing columns
            current_column += 1
        if token_type == "name" and token == "def" and not reading["function"]:
            current_idx["function"] = len(python_code)
            reading["function"] = True
        elif token_type == "name" and token == "class" and not reading["class"]:
            current_idx["class"] = len(python_code)
            reading["class"] = True
        # Save the name of the element
        if prev_token == "def" and name["function"] == None:
            name["function"] = token
        if prev_token == "class" and name["class"] == None:
            name["class"] = token
        # Append the token to the current code
        python_code += token
        # Check if finalised function or class
        for k, v in reading.items():
            if v and indents[k] == dedents[k] and indents[k] != 0:
                # Append new element
                stored[k].append(
                    (python_code[current_idx[k] :], name[k], docstring_pos[k])
                )
                # Reset params
                indents[k] = 0
                dedents[k] = 0
                reading[k] = False
                docstring_pos[k] = None
                name[k] = None
        # Update the current row and column
        current_row = end_row
        current_column = end_col
        # Save the previous token
        prev_token = token
    return stored, python_code


def read_content(file_path):
    """
    Reads the content of a text file.

    This function opens a specified file in read mode and returns its entire content as a string.
    It is important to ensure that the file exists and is accessible to avoid exceptions.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        (str): The content of the file as a string.
    """
    with open(file_path, "r") as file:
        return file.read()


def list_submodule_directories(project_directory):
    """
    Retrieves a list of submodule directory names from a specified Git project.

    This function executes the "git submodule status" command to fetch the status
    of submodules in a Git repository located at the specified project directory.
    It then processes the output to extract the names of the subdirectories that
    contain these submodules.

    Args:
        project_directory (str): The path to the Git project directory where
        submodules are to be checked.

    Returns:
        (list): A list of submodule directory names. If no submodules are found, an
            empty list is returned.
    """
    project_directory = Path(project_directory)
    submodule_directories = []
    try:
        # Use the "git submodule status" command to list submodules
        git_command = ["git", "submodule", "status"]
        result = subprocess.run(
            git_command,
            cwd=project_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        # Split the output into lines and extract submodule directory names
        output_lines = result.stdout.strip().split("\n")
        for line in output_lines:
            try:
                _, submodule_path, _ = line.split()
            except ValueError:  # TODO: Check error type
                LOGGER.info(
                    "%s\rNo git submodules found in the project", ANSI_CODE["reset"]
                )
                return submodule_directories
            submodule_name = Path(submodule_path).name
            submodule_directories.append(submodule_name)
    except subprocess.CalledProcessError:
        LOGGER.info("%s\rNo git submodules found in the project", ANSI_CODE["reset"])
    return submodule_directories


def is_file_in_directory(directory, name):
    """
    Checks if a file or directory with a specified name exists within a given directory.

    This function traverses the specified directory and all its subdirectories to search
    for a file or directory that matches the provided name. It returns True if a match is found,
    otherwise it returns False.

    Args:
        directory (str or Path): The path to the directory to search in.
        name (str): The name of the file or directory to look for.

    Returns:
        (bool): True if the file or directory exists in the directory, False otherwise.
    """
    directory = Path(directory)
    for item in directory.glob("**/*"):
        if item.is_dir() and item.name == name:
            return True
        elif item.is_file() and item.name == name:
            return True
    return False


def copy_path(path, add_to_parent="_formatted"):
    """
    Copies a file or directory to a new formatted path and creates a documented version if applicable.

    This function checks if the specified path exists and determines if it is a file or directory.
    If it is a file with a supported suffix, it copies the file to a new location, appending a
    specified string to the base filename. If the path points to a directory, it copies the
    directory and maintains the new formatted name. Error messages are logged for non-existent
    paths, files that cannot be documented, and existing paths.

    Args:
        path (str or Path): The path of the file or directory to copy.
        add_to_parent (str, optional): The string to append to the base name for the formatted file
            or directory (default is '_formatted').

    Returns:
        (Path): The path of the newly created formatted file or directory.
    """
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"{ANSI_CODE['red']}\r❌Error: '{path}' does not exist."
        )
    formatted_base_name = f"{path.stem}{add_to_parent}{path.suffix}"
    formatted_path = path.parent / formatted_base_name
    if path.is_file() and path.suffix in SUFFIX.values():
        try:
            shutil.copy(path, formatted_path)
            LOGGER.info(
                "%s\rFile %s copied and documented version is to be created: %s",
                ANSI_CODE["reset"],
                path.name,
                formatted_base_name,
            )
        except FileExistsError:
            LOGGER.info("%s\r⚠ The file {path} already exists.", ANSI_CODE["yellow"])
    elif path.is_file() and path.suffix not in SUFFIX.values():
        LOGGER.info(
            "%s\r❌ The script {path} can not be documented. Programming language not supported yet.",
            ANSI_CODE["red"],
        )
        return None
    elif path.is_dir():
        try:
            shutil.copytree(path, formatted_path)
            LOGGER.info(
                "%s\rDirectory {path.name} copied and formatted version created: {formatted_base_name}",
                ANSI_CODE["reset"],
            )
        except FileExistsError:
            LOGGER.info(
                "%s\r⚠ The folder {formatted_path} already exists.", ANSI_CODE["yellow"]
            )
    return formatted_path


def ensure_folder_exist(path):
    """
    Ensure that a folder path exists by creating any missing directories.

    This function takes a path as input, checks each segment of the path, and
    creates any directories that do not already exist. It supports both absolute
    and relative paths.

    Args:
        path (str): The path of the directory to ensure exists.

    Returns:
        (bool): True if the directory already existed, False if it was created.
    """
    path = str(path)
    separated = path.split(os.path.sep)
    # To consider absolute paths
    if separated[0] == "":
        separated.pop(0)
        separated[0] = os.path.sep + separated[0]
    exists = True
    for f in range(len(separated)):
        path = (
            os.path.sep.join(separated[: f + 1])
            if f > 0
            else (separated[0] + os.path.sep)
        )
        if not os.path.exists(path):
            os.mkdir(path)
            exists = False
    return exists


def get_temp_folder():
    """
    Retrieves the path to the temporary folder based on the operating system.

    This function checks the platform on which Python is running and returns the appropriate
    path for the temporary folder. For Windows, it uses the TEMP environment variable. For
    Linux and macOS (Darwin), it returns the standard "/tmp" directory. If the operating
    system is not recognized, it raises an OSError.

    Returns:
        (str): The path to the temporary folder.
    """
    system_platform = platform.system()
    if system_platform == "Windows":
        return os.environ["TEMP"]
    elif system_platform == "Linux" or system_platform == "Darwin":
        return "/tmp"
    else:
        raise OSError("Unsupported operating system")
