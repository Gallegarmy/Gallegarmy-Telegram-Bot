import logging, os, structlog

# Configuration of the logger
level = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_LEVEL = getattr(logging, level)
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVEL))
logger = structlog.get_logger()