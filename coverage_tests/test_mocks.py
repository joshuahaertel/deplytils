"""Make sure mocks respond to the interface as desired"""
from unittest import TestCase

from coverage import CoverageException

from putils.mocks import MockCoverage


# pragma pylint: disable=missing-docstring
# pylint: disable=unused-variable
class TestMockCoverage(TestCase):
    def test_good_report(self):
        report_value = 12.54
        coverage = MockCoverage(report=report_value)
        self.assertEqual(coverage.start(), None)
        self.assertEqual(coverage.stop(), None)
        self.assertEqual(coverage.report(), report_value)
        self.assertEqual(coverage.html_report(), report_value)
        self.assertEqual(coverage.xml_report(), report_value)

    def test_no_data(self):
        with self.assertRaises(CoverageException):
            MockCoverage().report()
