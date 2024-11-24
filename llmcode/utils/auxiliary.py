"""
This module provides utilities for formatting and documenting code files.

It includes functions to format code files, apply documentation functions based on
programming languages, and manage temporary file operations during the documentation process.

Functions:
    format_code: Formats and documents code files in the specified path.
    _apply_to_scripts: Applies a given function to scripts in a directory, handling temporary files.

Author: Francisco Javier Gañán
License File: https://github.com/javierganan99/LLMCode/blob/main/LICENSE
"""

from pathlib import Path
import shutil
import os
from threading import Event
from tqdm import tqdm
import llmcode.cfg.custom_params as custom_params
from .file_utils import (
    list_submodule_directories,
    is_file_in_directory,
    copy_path,
    ensure_folder_exist,
    get_temp_folder,
)
from .completion import get_completion
from . import ANSI_CODE, DOC_FUNCTION, SUFFIX, LANGUAGE, TQDM_BAR_FORMAT
from .logger import LOGGER


def format_code(
    path,
    exclude=custom_params.exclude,
    languages=custom_params.languages,
    elements2doc=custom_params.elements2doc,
    overwrite=custom_params.overwrite,
    stop_flag=Event(),
):
    languages_filtered = languages.copy()
    path = Path(path)
    assert path.exists(), f"{ANSI_CODE['red']}\r❌ {path} does not exist."
    if path.is_dir():
        for i, l in enumerate(languages):
            if l not in DOC_FUNCTION.keys():
                LOGGER.info(
                    "%s\r⚠ Language %s not yet supported for docummentation. The %s scripts will not be docummented!",
                    ANSI_CODE["yellow"],
                    l,
                    l,
                )
                languages_filtered.pop(i)
        # Check if the exclude folders exist, if there is an error stop the program to warn the user
        for e in exclude:
            assert is_file_in_directory(
                path, e
            ), f"{ANSI_CODE['red']}\r❌ Check the name of the file {e} that you want to exclude because it is not included in {path}, you could have make a typo!"
        exclude.extend(list_submodule_directories(path))
        if exclude:
            exc_str = " ".join(exclude)
            LOGGER.info(
                "%s\r⚠ Excluding the following files from the document process: %s",
                ANSI_CODE["yellow"],
                exc_str,
            )
    elif path.is_file() and (
        (path.suffix not in SUFFIX.values())
        or LANGUAGE[path.suffix] not in DOC_FUNCTION.keys()
    ):
        LOGGER.info(
            "%s\r❌ The script %s can not be documented. Programming language with extension %s not supported.",
            ANSI_CODE["red"],
            str(path),
            path.suffix,
        )
        return None
    new_path = (
        copy_path(path, add_to_parent=custom_params.surname)
        if not custom_params.rewrite
        else path
    )
    for l in languages_filtered:
        if stop_flag.is_set():
            break
        _apply_to_scripts(
            new_path,
            (
                DOC_FUNCTION[l]["function"]
                if path.is_dir()
                else DOC_FUNCTION[LANGUAGE[path.suffix]]["function"]
            ),
            extension=SUFFIX[l] if path.is_dir() else path.suffix,
            exclude=exclude,
            stop_flag=stop_flag,
            get_completion=get_completion,
            **{
                **DOC_FUNCTION[l]["kwargs"],
                "elements2doc": elements2doc,
                "overwrite": overwrite,
            },
        )
    return True


def _apply_to_scripts(
    root_path,
    function_to_execute,
    extension,
    exclude,
    stop_flag=Event(),
    *args,
    **kwargs,
):
    root_path = Path(root_path).resolve()
    if root_path.is_dir():
        files = [py_file.resolve() for py_file in root_path.glob(f"**/*{extension}")]
        if not files:
            LOGGER.info(
                "%s\r⚠ No scripts were found for %s in the folder %s",
                ANSI_CODE["yellow"],
                LANGUAGE[extension],
                str(root_path),
            )
            return None
        files = [
            file
            for file in files
            if not any([str(discard) in str(file) for discard in exclude])
        ]
        # Create temporary project
        temporary_files = []
        temporary_folders = []
        for file in files:
            folder_name = str(file.parent).replace(
                str(root_path), get_temp_folder() + os.path.sep + str(root_path.name)
            )
            ensure_folder_exist(folder_name)
            temporary_folders.append(folder_name)
            temporary_files.append(Path(folder_name) / file.name)
        temporary_folders = list(set(temporary_folders))  # Get unique elements
        # Copy the files to the temporary dir
        for f, tf in zip(files, temporary_files):
            shutil.copyfile(f, tf)
        pbar = tqdm(
            temporary_files,
            desc=f"{ANSI_CODE['reset']}\rStarting to document...",
            total=len(temporary_files),
            bar_format=TQDM_BAR_FORMAT,
        )
        for c_file in pbar:
            pbar.set_description(
                f"{ANSI_CODE['reset']}\rDocumenting script {c_file}..."
            )
            function_to_execute(c_file, stop_flag=stop_flag, *args, **kwargs)
            if stop_flag.is_set():
                LOGGER.info(
                    "%s\r Terminated by user. Program was documenting script %s",
                    ANSI_CODE["yellow"],
                    str(c_file),
                )
                break
        pbar.close()
        # Copy the files to the original location and delete the temporary file
        for f, tf in zip(files, temporary_files):
            shutil.copyfile(tf, f)
            os.remove(tf)
    else:
        folder_name = str(root_path.parent).replace(
            str(root_path.parent),
            get_temp_folder() + os.path.sep + str(root_path.parent.name),
        )
        ensure_folder_exist(folder_name)
        file = Path(folder_name) / root_path.name
        shutil.copyfile(root_path, file)
        function_to_execute(file, stop_flag=stop_flag, *args, **kwargs)
        shutil.copyfile(file, root_path)
        os.remove(file)
    return True
