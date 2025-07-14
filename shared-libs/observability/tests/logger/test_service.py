from observability.logging import LoggingService


def test_logger_creation() -> None:
    logger = LoggingService().get_logger("test")
    assert logger.name == "test"
