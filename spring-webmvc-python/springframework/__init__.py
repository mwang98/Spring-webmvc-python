import os
import logging


def configure_logging():
    logging_level = os.getenv("LOGGING_LEVEL", "INFO").upper()
    numeric_level = getattr(logging, logging_level, None)

    if not isinstance(numeric_level, int):
        raise Exception(f"Invalid log level: {numeric_level}")

    logging.basicConfig(
        level=numeric_level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s] [%(process)s] [%(levelname)s] [%(module)s]: %(message)s",
    )
    logging.info(f"Logging level: {logging_level}")


configure_logging()
