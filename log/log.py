import logging


def config_logging(
        level: int = logging.DEBUG, **kwargs) -> None:
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%dT%H:%M:%S.%s+0800',
        **kwargs
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
