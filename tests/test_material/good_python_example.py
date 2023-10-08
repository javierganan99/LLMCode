from pathlib import Path
from pathlib import Path
import LLMCode.cfg.custom_params as custom_params
from .file_utils import (
    list_submodule_directories,
    is_file_in_directory,
    copy_path,
    ensure_folder_exist,
    get_temp_folder,
)
from .completion import get_completion
from . import DOC_FUNCTION
from . import ANSI_CODE, SUFFIX, TQDM_BAR_FORMAT
from tqdm import tqdm


class ExampleClass:
    def __init__(self):
        self.variable = True

    def example_method(self, param):
        print(param)


def format_code(path, exclude, languages, stop_flag):
    languages_filtered = languages.copy()
    for i, l in enumerate(languages):
        if l not in DOC_FUNCTION.keys():
            print(
                f"{ANSI_CODE['yellow']}\r Language {l} not yet supported for docummentation. The {l} scripts will not be docummented!"
            )
            languages_filtered.pop(i)
    if Path(path).is_dir():
        # Check if the exclude folders exist, if there is an error stop the program to warn the user
        for e in exclude:
            assert is_file_in_directory(
                path, e
            ), f"{ANSI_CODE['red']}\r Check the name of the folder {e} that you want to exclude because it is not included in {path}, you could have make a typo!"
        exclude.extend(list_submodule_directories(path))
        if exclude:
            exc_str = " ".join(exclude)
            print(
                f"{ANSI_CODE['yellow']}\r Excluding the following files from the document process: {exc_str}"
            )
    new_path = (
        copy_path(path, add_to_parent=vars(custom_params)["surname"])
        if not vars(custom_params)["rewrite"]
        else path
    )
    for l in languages_filtered:
        if stop_flag.is_set():
            break
        apply_to_scripts(
            new_path,
            DOC_FUNCTION[l],
            extension=SUFFIX[l],
            exclude=exclude,
            stop_flag=stop_flag,
            get_completion=get_completion,
        )
