import logging.config

logger = logging.getLogger(__name__)


def configure_logging(logging_config: dict):
    logging.config.dictConfig(logging_config)
    logger.info("Logging configured successfully")
