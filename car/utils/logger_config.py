import logging

def setup_logger(name, log_file='carbot.log', level=logging.DEBUG):
    """
    Sets up a logger with both file and console output.

    :param name: Name of the logger.
    :param log_file: Log file path.
    :param level: Logging level (default is DEBUG).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler for logging to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatter for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger if they haven't been added already
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
