import logging
from logging.config import dictConfig
from pathlib import Path


def setup_logging(env: str = "production"):
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_files = ["app.log", "error.log"]
    for log_file in log_files:
        log_path = log_dir / log_file
        if not log_path.exists():
            log_path.touch()

    # Set log level based on environment
    log_levels = {
        "production": "WARNING",
        "staging": "INFO",
        "development": "DEBUG",
    }
    log_level = log_levels.get(env, "INFO")

    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(asctime)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(asctime)s | %(client_addr)s - "%(request_line)s" %(status_code)s',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_dir / "app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
            },
            "error_file": {
                "formatter": "default",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": log_dir / "error.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8",
                "level": "ERROR",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default", "file", "error_file"],
                "level": log_level,
            },
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }

    # Apply the logging configuration
    dictConfig(log_config)

    # Create and return logger instance
    logger = logging.getLogger("fastapi_app")
    return logger, log_config
