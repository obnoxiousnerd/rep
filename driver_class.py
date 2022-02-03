import logging
from os import path
from sys import stdout
from colorama import Fore, Style
import yaml


class LogFormatter(logging.Formatter):
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
    colors = {
        logging.DEBUG: log_format,
        logging.INFO: Fore.CYAN + log_format + Fore.RESET,
        logging.WARN: Fore.YELLOW + log_format + Fore.RESET,
        logging.ERROR: Fore.RED + log_format + Fore.RESET,
        logging.FATAL: Fore.RED + Style.BRIGHT + log_format + Fore.RESET,
    }

    def format(self, record):
        color = self.colors.get(record.levelno)
        formatter = logging.Formatter(color)
        return formatter.format(record)


log_stream = logging.StreamHandler(stdout)
log_stream.setFormatter(LogFormatter())


class Config:
    """
    Config is a singleton used across the whole application
    to load configuration settings.
    """

    __config__ = None

    def __new__(cls):
        # Since this class is a singleton, the __new__ method is overrided
        # to make it behave likewise.
        if cls.__config__ is None:
            instance = super(Config, cls).__new__(cls)
            cls.__config__ = instance.__load__()
        return cls.__config__

    def __load__(self):
        if self.__config__ is None:
            # Cache the parsed config.
            self.__config__ = yaml.safe_load(
                open(path.join("config", "config.yml"), "r")
            )
        return self.__config__


class GenericDriver:
    """
    GenericDriver is a base class for all application driver classes.
    Extend this class for all sub-generic driver classes.
    """

    def __init__(self, config: dict) -> None:
        self.config = config
        self.logger = logging.Logger(self.__class__.__name__, logging.DEBUG)
        self.logger.addHandler(log_stream)
        self.logger.setLevel(logging.DEBUG)


class DataDriver(GenericDriver):
    """
    DataDriver is a generic base class for all driver classes that fetch the data
    required for generating.
    """

    def load(self):
        pass


class Renderer(GenericDriver):
    """
    Renderer is a generic base class for all driver classes that render the data
    into suitable format.
    """

    def render(self, data):
        pass

class EmailDriver(GenericDriver):
    """
    EmailDriver is a generic base class for all driver classes that send the
    rendered data to the email address.
    """

    def send(self, data):
        pass