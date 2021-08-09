import os

DEFAULT_LOG_FORMAT = os.environ.get(
    "DEFAULT_LOG_FORMAT",
    "%(asctime)s (%(filename)s, %(funcName)s, %(lineno)d) [%(levelname)8s] %(message)s",
)
DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


def get_default_log_format():
    return DEFAULT_LOG_FORMAT


def get_default_log_level():
    return DEFAULT_LOG_LEVEL
