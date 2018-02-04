"""Test Context Managers"""
import importlib
from unittest import TestCase

from coverage import CoverageException

from putils.contexts import coverage
from coverage_tests import coverage_fixture


# pragma pylint: disable=missing-docstring,unused-variable
# noinspection PyMissingOrEmptyDocstring
class BaseCoverage(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module_path = 'tests.coverage_fixture'
        cls.module_name = '{}.py'.format(cls.module_path)


class TestCoverageContext(BaseCoverage):
    def test_not_silent__no_report(self):
        """
        Outputting to file goes to a file, not stdout, so it can't be
        silenced
        """
        with self.assertRaises(AssertionError):
            with coverage.CoverageContext(
                    report_type='file_report', silent=True, report_kwargs={}):
                importlib.reload(coverage_fixture)

    @staticmethod
    def test_no_report():
        with coverage.CoverageContext(report=False):
            importlib.reload(coverage_fixture)

    @staticmethod
    def test_silent_report():
        with coverage.CoverageContext(silent=True):
            importlib.reload(coverage_fixture)


class TestStrictCoverage(BaseCoverage):
    def test_meet_threshold(self):
        coverage.StrictCoverage()
        with coverage.StrictCoverage(coverage_kwargs=dict(
                config_file='.ccoveragerc', source=(self.module_path,)),
                silent=False, mock_kwargs=dict(report=100.0)):
            importlib.reload(coverage_fixture)
            instance = coverage_fixture.CoverageFixture()
            instance.run()

    def test_miss_threshold(self):
        with self.assertRaises(CoverageException):
            with coverage.StrictCoverage(coverage_kwargs=dict(
                    config_file='.ccoveragerc', source=(self.module_path,)),
                    mock_kwargs=dict(report=80.0)):
                importlib.reload(coverage_fixture)
                coverage_fixture.CoverageFixture()
