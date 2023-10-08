import shutil
import subprocess
from pathlib import Path
from . import ANSI_CODE, SUFFIX
from tokenize import tokenize
from token import tok_name
import os
import platform


def parse_python(fn):
    fp = open(fn, mode="rb")
    try:
        toks = list(tokenize(fp.readline))
        for tok in toks:
            if tok_name[tok.type] == "ERRORTOKEN":
                raise Exception(
                    f"{ANSI_CODE['red']}\r❌ Check the script {fn}. It contains errors."
                )
    except Exception as e:
        raise Exception("Script could not be tokenized") from e
    finally:
        fp.close()
    toks.pop(0)
    return toks


def extract_functions_and_classes_from_python_tokens(tokens):
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
    with open(file_path, "r") as file:
        return file.read()


def list_submodule_directories(project_directory):
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
            _, submodule_path, _ = line.split()
            submodule_name = Path(submodule_path).name
            submodule_directories.append(submodule_name)
    except subprocess.CalledProcessError as e:
        print(f"{ANSI_CODE['reset']}\rNo git submodules found in the project")
    return submodule_directories


def is_file_in_directory(directory, name):
    directory = Path(directory)
    for item in directory.glob("**/*"):
        if item.is_dir() and item.name == name:
            return True
        elif item.is_file() and item.name == name:
            return True
    return False


def copy_path(path, add_to_parent="_formatted"):
    path = Path(path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"{ANSI_CODE['red']}\r❌Error: '{path}' does not exist.")
    formatted_base_name = f"{path.stem}{add_to_parent}{path.suffix}"
    formatted_path = path.parent / formatted_base_name
    if path.is_file() and path.suffix in SUFFIX.values():
        try:
            shutil.copy(path, formatted_path)
            print(
                f"{ANSI_CODE['reset']}\rFile {path.name} copied and documented version is to be created: {formatted_base_name}"
            )
        except FileExistsError as e:
            print(f"{ANSI_CODE['yellow']}\r⚠ The file {path} already exists.")
    elif path.is_file() and path.suffix not in SUFFIX.values():
        print(
            f"{ANSI_CODE['red']}\r❌ The script {path} can not be documented. Programming language not supported yet."
        )
        return None
    elif path.is_dir():
        try:
            shutil.copytree(path, formatted_path)
            print(
                f"{ANSI_CODE['reset']}\rDirectory {path.name} copied and formatted version created: {formatted_base_name}"
            )
        except FileExistsError as e:
            print(
                f"{ANSI_CODE['yellow']}\r⚠ The folder {formatted_path} already exists."
            )
    return formatted_path


def ensure_folder_exist(path):
    path = str(path)
    separated = path.split(os.path.sep)
    # To consider absolute paths
    if separated[0] == "":
        separated.pop(0)
        separated[0] = os.path.sep + separated[0]
    exists = True
    for f in range(len(separated)):
        path = os.path.join(*separated[: f + 1])
        if not os.path.exists(path):
            os.mkdir(path)
            exists = False
    return exists


def get_temp_folder():
    system_platform = platform.system()
    if system_platform == "Windows":
        return os.environ["TEMP"]
    elif system_platform == "Linux" or system_platform == "Darwin":
        return "/tmp"
    else:
        raise Exception("Unsupported operating system")
