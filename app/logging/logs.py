import logging


def configure_logging():
    logger = logging.getLogger()
    logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
