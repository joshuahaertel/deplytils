"""File for Mock objects -- primarily used for testing purposes"""
from coverage import CoverageException


class MockCoverage(object):  # pylint: disable=unused-variable
    """
    Mock Coverage Object. Aside from testing, it has a another use
    based on the problems that can occur when a Coverage runs inside
    of Coverage (a coverage inception space time continuum). It
    matches the interface but fails to run due to the complications
    that can occur.
    """

    def __init__(self, report=None):
        """
        Init the MockCoverage object. For now, it does not accept the
        same arguments, however, this may be needed in the future.

        :param report: value to return in the report
        """
        self.report_value = report

    def start(self):
        """Pretend to start"""
        pass

    def stop(self):
        """Pretend to stop"""
        pass

    def report(self, *_, **__):
        """Pretend to report"""
        if self.report_value is None:
            raise CoverageException("No data to report.")
        return self.report_value

    def html_report(self, *_, **__):
        """Pretend to output HTML files"""
        return self.report()

    def xml_report(self, *_, **__):
        """Pretend to output XML"""
        return self.report()
