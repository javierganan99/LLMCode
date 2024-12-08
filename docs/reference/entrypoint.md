# Reference for `llmcode/entrypoint.py`

This module serves as the entry point for the LLMCode tool. It parses
command-line arguments to determine the path to format, any directories or files
to exclude, the programming languages to include, and the elements to document.
It also handles the option to overwrite existing docstrings.

Options:
    path            The path to the script or folder to be documented.
    --exclude       Exclude specific files or folders from the path.
    --languages     Specify programming languages to include.
    --elements2doc  Specify elements to document.
    --overwrite     Overwrite existing docstrings if present.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE

<br>

## ::: llmcode.entrypoint.parse_args

<br><br><hr><br>

## ::: llmcode.entrypoint.main

<br><br>
