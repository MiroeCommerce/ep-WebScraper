import os
import sys
import json
from loguru import logger


def serialize(record):
    subset = {
        "timestamp": record["time"].strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "level": record["level"].name,
        "message": record["message"],
        "module": record["module"],
        "function": record["function"],
    }
    if record["extra"]:
        subset.update(record["extra"])
    if record["exception"]:
        subset["exception_type"] = record["exception"].type.__name__
        subset["exception_message"] = str(record["exception"].value)
        subset["stack_trace"] = "".join(record["exception"].traceback.format())
    return json.dumps(subset)


def formatter(record):
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


def setup_logger():
    logger.remove()

    level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_to_stdout = os.getenv("LOG_TO_STDOUT", "True").lower() == "true"
    log_file = os.getenv("LOG_FILE", "logs/logger.log")
    log_rotation = os.getenv("LOG_ROTATION", "10 MB")
    log_retention = os.getenv("LOG_RETENTION", "7 days")
    log_compression = os.getenv("LOG_COMPRESSION", "zip")

    if log_to_stdout:
        logger.add(
            sys.stdout,
            level=level,
            format="{time} | {level} | <level> {message} </level> ",
        )

    logger.add(
        log_file,
        level=level,
        format=formatter,
        rotation=log_rotation,
        retention=log_retention,
        compression=log_compression,
    )
