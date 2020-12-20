"""Tests helpers module"""

import pytest
from aws_lambda_powertools.utilities.parameters.exceptions import GetParameterError

from fast_app.helpers.helpers import get_ssm_parameter


def test_invalid_ssm_parameter_with_default():
    """Test get_ssm_parameter retrieves default value"""
    param_value = get_ssm_parameter(
        ssm_parameter_key="/oops/not/valid", default="NoWorries"
    )
    assert param_value == "NoWorries"


def test_invalid_ssm_parameter_without_default():
    """Test get_ssm_parameter raises an error when no default value provided"""
    with pytest.raises(GetParameterError):
        _ = get_ssm_parameter(ssm_parameter_key="/oops/not/valid")
