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
