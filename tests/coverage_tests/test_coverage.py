"""Test Context Managers"""
import importlib
from unittest import TestCase

import six
from coverage import CoverageException

from putils.contexts import coverage
from tests.coverage_tests import coverage_fixture


# pragma pylint: disable=missing-docstring,unused-variable
# noinspection PyMissingOrEmptyDocstring
class BaseCoverage(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module_path = 'tests.coverage_fixture'
        cls.module_name = '{}.py'.format(cls.module_path)

    @staticmethod
    def _reload_import():
        if six.PY2:
            reload(coverage_fixture)  # pylint: disable=undefined-variable
        else:
            importlib.reload(coverage_fixture)  # pylint: disable=no-member


class TestCoverageContext(BaseCoverage):
    def test_not_silent__no_report(self):
        """
        Outputting to file goes to a file, not stdout, so it can't be
        silenced
        """
        with self.assertRaises(AssertionError):
            with coverage.CoverageContext(
                    report_type='file_report', silent=True, report_kwargs={}):
                self._reload_import()

    def test_no_report(self):
        with coverage.CoverageContext(report=False):
            self._reload_import()

    def test_silent_report(self):
        with coverage.CoverageContext(silent=True):
            self._reload_import()


class TestStrictCoverage(BaseCoverage):
    def test_meet_threshold(self):
        coverage.StrictCoverage(100)
        with coverage.StrictCoverage(100, coverage_kwargs=dict(
                config_file='.coveragerc', source=(self.module_path,)),
                silent=False, mock_kwargs=dict(report=100.0)):
            self._reload_import()
            instance = coverage_fixture.CoverageFixture()
            instance.run()

    def test_miss_threshold(self):
        with self.assertRaises(CoverageException):
            with coverage.StrictCoverage(100, coverage_kwargs=dict(
                    config_file='.coveragerc', source=(self.module_path,)),
                    mock_kwargs=dict(report=80.0)):
                self._reload_import()
                coverage_fixture.CoverageFixture()
