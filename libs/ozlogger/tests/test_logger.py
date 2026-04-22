import logging
from ozlogger import get_logger


def test_get_logger_returns_logger():
    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)


def test_get_logger_level_is_info():
    logger = get_logger("test.level")
    assert logger.level == logging.INFO


def test_get_logger_same_instance():
    assert get_logger("test.same") is get_logger("test.same")
