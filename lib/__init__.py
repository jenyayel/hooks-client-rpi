"""
Core functionality of hooks client
"""

import os
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": '[%(asctime)s: %(levelname)s/%(name)s] %(message)s'
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
            "filters": []
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "propagate": 0,
            "handlers": ["console"]
        },
        "requests.packages.urllib3.connectionpool": {
            "level": "WARNING",
            "propagate": 0,
            "handlers": ["console"]
        },
        "lib.service_bus.client": {
            "level": "DEBUG",
            "propagate": 0,
            "handlers": ["console"]
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
