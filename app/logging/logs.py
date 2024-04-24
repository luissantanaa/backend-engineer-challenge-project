import logging


def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a console handler with a higher log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it to both handlers
    formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)

    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
