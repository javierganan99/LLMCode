import platform
import logging.config
import os

MACOS, LINUX, WINDOWS = (
    platform.system() == x for x in ["Darwin", "Linux", "Windows"]
)  # environment booleans

LOGGING_NAME = "LLMCode"


def set_logging(name=LOGGING_NAME, verbose=True):
    rank = int(os.getenv("RANK", -1))  # rank in world for Multi-GPU
    level = logging.INFO if verbose and rank in {-1, 0} else logging.ERROR
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {name: {"format": "%(message)s"}},
            "handlers": {
                name: {
                    "class": "logging.StreamHandler",
                    "formatter": name,
                    "level": level,
                }
            },
            "loggers": {name: {"level": level, "handlers": [name], "propagate": False}},
        }
    )


def emojis(string=""):
    """Return platform-dependent emoji-safe version of string."""
    return string.encode().decode("ascii", "ignore") if WINDOWS else string


class EmojiFilter(logging.Filter):
    """
    A custom logging filter class for removing emojis in log messages.

    This filter is particularly useful for ensuring compatibility with Windows terminals
    that may not support the display of emojis in log messages.
    """

    def filter(self, record):
        """Filter logs by emoji unicode characters on windows."""
        record.msg = emojis(record.msg)
        return super().filter(record)


# Set logger
set_logging(LOGGING_NAME, verbose=True)  # run before defining LOGGER
LOGGER = logging.getLogger(LOGGING_NAME)
if WINDOWS:  # emoji-safe logging
    LOGGER.addFilter(EmojiFilter())
