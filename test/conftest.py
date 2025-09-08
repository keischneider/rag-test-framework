def pytest_addoption(parser):
    parser.addoption(
        "--eval_type",
        action="store",
        default="default_value",
        help="A single value"
    )
    parser.addoption(
        "--langs",
        action="store",
        nargs="+",
        help="List of languages"
    )

import pytest


@pytest.fixture
def eval_type(request):
    return request.config.getoption("--eval_type")


@pytest.fixture
def langs(request):
    return request.config.getoption("--langs")