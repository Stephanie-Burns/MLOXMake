
import pytest

from src.MLOXMaker.managers.app_log import AppLog


def pytest_configure(config):
    """Automatically enable test mode in AppLog when pytest runs."""
    AppLog.testing_mode = True
