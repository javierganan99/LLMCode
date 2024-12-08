"""
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
"""

import sys
import argparse
import signal
from threading import Event
from llmcode.cfg.custom_params import exclude, languages, elements2doc
from .utils.logger import LOGGER
from .utils.auxiliary import format_code


def parse_args():
    """
    Parses command-line arguments for the script.

    This function sets up an argument parser to handle the input parameters
    required for the script execution. It allows the user to specify a path,
    exclude certain files or directories, choose programming languages,
    identify elements to document, and decide whether to overwrite existing
    docstrings.

    Args:
        path (str, optional): The path to format without a name (default is None).
        --exclude (str, optional): A list of files or folders to exclude (default is exclude).
        --languages (str, optional): A list of programming languages to include (default is languages).
        --elements2doc (str, optional): A list of elements to document (default is elements2doc).
        --overwrite (bool, optional): Whether to overwrite the current docstrings (default is False).

    Returns:
        Namespace: An object containing the parsed arguments as attributes.
    """
    parser = argparse.ArgumentParser(
        description="The first param is the path to format but with no name. \
            You can add the --exclude param to exclude some dirs or files"
    )
    parser.add_argument("path", nargs="?", default=None, help="Unnamed parameter")
    parser.add_argument(
        "--exclude",
        nargs="*",
        default=exclude,
        help="Exclude some files or folders inside the path",
    )
    parser.add_argument(
        "--languages",
        nargs="*",
        default=languages,
        help="The programming languages you want to include",
    )
    parser.add_argument(
        "--elements2doc",
        nargs="*",
        default=elements2doc,
        help="The elements2doc names you want to document",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Wheter to overwrite or not the current docstrings",
    )
    return parser.parse_args()


def main():
    """
    Main function to initiate the formatting process for scripts or folders.

    This function sets up a signal handler for interrupt signals (SIGINT) to gracefully stop the operation
    when requested. It checks for the required path argument, and if missing, logs an informative message
    and exits. It then calls the `format_code` function with the appropriate parameters.
    """

    def crtl_c_handler(sig, frame):
        stop_flag.set()

    signal.signal(signal.SIGINT, crtl_c_handler)
    stop_flag = Event()
    args = parse_args()
    if args.path is None:
        LOGGER.info(
            "Missing path to format: Please provide the path to be documented. \
            It can be an script or a folder containing scripts at any level."
        )
        sys.exit(0)
    format_code(
        args.path,
        args.exclude,
        args.languages,
        args.elements2doc,
        args.overwrite,
        stop_flag,
    )


if __name__ == "__main__":
    main()
