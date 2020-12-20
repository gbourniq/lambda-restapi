"""
This module defines the logger and metrics objects
"""


from aws_lambda_powertools import Logger, Metrics

from lambda_restapi.core.config import (
    LOG_LEVEL,
    POWERTOOLS_METRICS_NAMESPACE,
    POWERTOOLS_SERVICE_NAME,
)

logger = Logger(service=POWERTOOLS_SERVICE_NAME, level=LOG_LEVEL)

metrics = Metrics(
    service=POWERTOOLS_SERVICE_NAME, namespace=POWERTOOLS_METRICS_NAMESPACE,
)
