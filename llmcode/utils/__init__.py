"""
This module initializes utility constants and functions for the application.
It defines file suffixes, language mappings, ANSI color codes, and document functions.

Attributes:
    SUFFIX (dict): Maps programming languages to their file suffixes.
    LANGUAGE (dict): Maps file suffixes to their corresponding programming languages.
    ANSI_CODE (dict): ANSI escape codes for terminal text coloring.
    TQDM_BAR_FORMAT (str): Format string for tqdm progress bars.
    DOC_FUNCTION (dict): Maps programming languages to their document functions and parameters.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

SUFFIX = {"python": ".py", "c++": ".cpp"}
LANGUAGE = {".py": "python", ".cpp": "c++"}
ANSI_CODE = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "reset": "\u001b[0m",
}
TQDM_BAR_FORMAT = "{desc}: {percentage:3.0f}%|{bar:20}| {n_fmt}/{total_fmt} [{elapsed}]"

from .document import doc_python_file
from ..cfg.custom_params import document_prompts

DOC_FUNCTION = {
    "python": {
        "function": doc_python_file,
        "kwargs": {"prompts": document_prompts["python"]},
    }
}
