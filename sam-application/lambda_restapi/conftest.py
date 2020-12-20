"""This file defines pytest fixtures"""

import json
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict

import pytest
from aws_lambda_powertools.utilities.typing import LambdaContext

from fast_app.constants import ImplementedHttpMethods

ROOT_DIR = Path(__file__).resolve().parent
API_EVENT_JSON = ROOT_DIR / "test_events/mock-api-gtw-event.json"
LAMBDA_CONTEXT_JSON = ROOT_DIR / "test_events/mock-lambda-context.json"


@pytest.fixture()
def mock_base_get_event() -> Dict[str, Any]:
    """ Base Mock API GW Event for a GET request"""
    with open(API_EVENT_JSON) as json_file:
        base_get_event = json.load(json_file)
    base_get_event["httpMethod"] = ImplementedHttpMethods.GET.value
    base_get_event["requestContext"]["httpMethod"] = ImplementedHttpMethods.GET.value
    return base_get_event


@pytest.fixture()
def mock_base_post_event() -> Dict[str, Any]:
    """ Base Mock API GW Event for a POST request"""
    with open(API_EVENT_JSON) as json_file:
        base_post_event = json.load(json_file)
    base_post_event["httpMethod"] = ImplementedHttpMethods.POST.value
    base_post_event["requestContext"]["httpMethod"] = ImplementedHttpMethods.POST.value
    return base_post_event


@pytest.fixture()
def mock_context() -> LambdaContext:
    """Generates a mock context"""
    with open(LAMBDA_CONTEXT_JSON) as json_file:
        lambda_context = json.load(json_file)
    return namedtuple("LambdaContext", lambda_context.keys())(*lambda_context.values())
