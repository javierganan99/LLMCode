"""
This module defines the custom parameters for configuring the documentation process
in LLMCode. It includes settings for file exclusion, language specification,
timeout settings, and documentation prompts.

Attributes:
    exclude (list): Files to exclude from documentation.
    elements2doc (list or None): Specific elements to document.
        If None, all elements are documented.
    languages (list): Languages of the scripts to be documented.
    completion_timeout (int): Maximum time to wait for the model to give a response (in seconds).
    rewrite (bool): Whether to overwrite the code in the same input path.
    surname (str): Suffix to add to the folder or file name if not overwriting.
    overwrite (bool): Whether to overwrite the current docstrings.
    document_prompts (dict): Paths to the prompt files for documenting functions and classes.
    query_completion_key (str): Placeholder in the prompt for an element.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

from pathlib import Path
import os

exclude = []
elements2doc = None
languages = ["python"]
completion_timeout = 30
rewrite = True
surname = "_analysed"
overwrite = False
document_prompts = {
    "python": {
        "function": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}python{os.path.sep}documentFunction.txt",
        "class": Path(__file__).parent
        / f"..{os.path.sep}prompts{os.path.sep}python{os.path.sep}documentClass.txt",
    }
}
query_completion_key = "!<QUERY COMPLETION>!"
