import logging
from abc import ABC, abstractmethod
from typing import Optional, Text

import structlog


class Logger(ABC):

    @abstractmethod
    def info(self, message: Text, **kwargs):
        pass

    @abstractmethod
    def warning(self, message: Text, **kwargs):
        pass

    @abstractmethod
    def error(self, message: Text, **kwargs):
        pass

    @abstractmethod
    def debug(self, message: Text, **kwargs):
        pass


class NullLogger(Logger):

    def info(self, message: Text, **kwargs):
        pass

    def warning(self, message: Text, **kwargs):
        pass

    def error(self, message: Text, **kwargs):
        pass

    def debug(self, message: Text, **kwargs):
        pass


class JsonStructuredLogger(Logger):

    def __init__(self, level: Optional[int] = None):
        if level is None:
            level = logging.WARNING

        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.StackInfoRenderer(),
                structlog.dev.set_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.processors.EventRenamer("message"),
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(level),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=False
        )
        self.logger = structlog.get_logger()

    def info(self, message: Text, **kwargs):
        self.logger.info(message, **kwargs)

    def warning(self, message: Text, **kwargs):
        self.logger.warning(message, **kwargs)

    def error(self, message: Text, **kwargs):
        self.logger.error(message, **kwargs)

    def debug(self, message: Text, **kwargs):
        self.logger.debug(message, **kwargs)
