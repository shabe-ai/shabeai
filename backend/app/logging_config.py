import logging
import sys

import structlog


def setup_logging():
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
    )
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        stream=sys.stdout,
    ) 