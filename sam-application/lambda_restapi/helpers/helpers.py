"""
This module defines various helper functions, and the
logger and metrics objects
"""
import json
from typing import Dict, List, Optional, Union

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.parameters.exceptions import GetParameterError

from fast_app.constants import PowertoolsVariables

# if PowertoolsVariables.BOTOCORE_LEVEL_LOGGING.value:
#     boto3.set_stream_logger()
#     boto3.set_stream_logger("botocore")

logger = Logger(
    service=PowertoolsVariables.POWERTOOLS_SERVICE_NAME.value,
    level=PowertoolsVariables.LOG_LEVEL.value,
)

metrics = Metrics(
    service=PowertoolsVariables.POWERTOOLS_SERVICE_NAME.value,
    namespace=PowertoolsVariables.POWERTOOLS_METRICS_NAMESPACE.value,
)


def get_ssm_parameter(
    ssm_parameter_key: str, default: Optional[Union[str, List[str]]] = None
) -> Union[str, List[str]]:
    """
    Wrapper around the get_parameter function to set a default value if
    a GetParameterError exception is raised and a default value is provided
    via the `default` argument.
    """
    try:
        data = parameters.get_parameter(ssm_parameter_key)
        logger.info(f"Retrieved value for SSM Parameter {ssm_parameter_key}")
    except GetParameterError as get_param_err:
        logger.error(f"Unable to retrieve SSM Parameter {ssm_parameter_key}")
        if default:
            logger.warning(f"Using default value {default} for {ssm_parameter_key}")
            return default
        raise get_param_err
    return data


def build_response(status_code: int, body: Dict) -> Dict[str, str]:
    """Build a single response schema for all endpoints"""
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
    }
