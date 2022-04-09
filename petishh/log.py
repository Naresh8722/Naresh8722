import logging


def NewLogger(name=None):
    log_file = 'locsrv.log'
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    loggerName = "{}".format(name)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    return logger