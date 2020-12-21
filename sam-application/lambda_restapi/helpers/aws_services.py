"""
This module defines various helper functions to communicate with AWS services
"""
from typing import List, Optional, Union

import boto3
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.parameters.exceptions import GetParameterError

from lambda_restapi.core.logging import logger


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


def get_s3_client():
    """Return a boto3 s3 client"""
    return boto3.client("s3")
