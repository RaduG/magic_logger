import importlib
import logging
import os
import sys
import textwrap
from tempfile import mkstemp
from unittest.mock import patch

import pytest

import magic_logger
from magic_logger import logger

MOCK_MODULE_NAME = "some_package.some_module"


@pytest.fixture(scope="module")
def mock_module():
    """
    Create a temporary module and import it using importlib so that we can test that
    our magic logger returns the correct attribute.

    Yields:
        types.ModuleType
    """
    module_code = """
    from magic_logger import logger
    def func(attr):
        return getattr(logger, attr)
    """

    handle, path = mkstemp(suffix=".py")
    f = os.fdopen(handle, "w")
    f.write(textwrap.dedent(module_code))
    f.close()

    # Import module
    spec = importlib.util.spec_from_file_location(MOCK_MODULE_NAME, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[MOCK_MODULE_NAME] = module
    spec.loader.exec_module(module)

    yield module

    # Delete file after the tests ran
    os.remove(path)


@pytest.mark.parametrize(["attr"], [["debug"], ["info"], ["warn"], ["getChild"]])
def test_logger_dispatches_to_correct_logger_in_imported_module(mock_module, attr):
    returned_attribute = mock_module.func(attr)
    expected_attribute = getattr(logging.getLogger(MOCK_MODULE_NAME), attr)

    assert returned_attribute == expected_attribute


@pytest.mark.parametrize(["attr"], [["debug"], ["info"], ["warn"], ["getChild"]])
def test_logger_dispatches_to_correct_logger_in_main_module(mock_module, attr, monkeypatch):
    monkeypatch.setattr(mock_module, "__name__", "__main__")

    returned_attribute = mock_module.func(attr)
    expected_attribute = getattr(logging.getLogger(MOCK_MODULE_NAME), attr)

    assert returned_attribute == expected_attribute


@pytest.mark.parametrize(
    ["method", "expected_to_call", "args", "kwargs"],
    [
        (logger.dict_config, "dictConfig", (1, 2, 3), {"arg1": "val1"}),
        (logger.file_config, "fileConfig", (1, 2, 3), {"arg1": "val1"}),
        (logger.listen, "listen", (1, 2, 3), {"arg1": "val1"}),
        (logger.stop_listening, "stopListening", (1, 2, 3), {"arg1": "val1"}),
    ],
)
def test_logger_dispatches_to_correct_config_function(method, expected_to_call, args, kwargs):
    with patch.object(magic_logger.logging.config, expected_to_call) as mocked:
        method(*args, **kwargs)

    mocked.assert_called_once_with(*args, **kwargs)
