import sys
import argparse
import signal
from threading import Event
from LLMCode.cfg.custom_params import exclude, languages, elements2doc
from .utils.logger import LOGGER
from .utils.auxiliary import format_code


def parse_args():
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
    def crtlC_handler(sig, frame):
        stop_flag.set()

    signal.signal(signal.SIGINT, crtlC_handler)
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
