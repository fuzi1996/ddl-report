import logging


class LogMode:
    _SELF_SET_MODE = None

    def set_self_set_mode(value):
        _SELF_SET_MODE = None

    @staticmethod
    def get_self_set_mode():
        return LogMode._SELF_SET_MODE


def config_logging(
        level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%dT%H:%M:%S.%s+0800'
    )


if LogMode.get_self_set_mode() is None:
    config_logging(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
