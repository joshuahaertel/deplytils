"""Context Managers"""
from __future__ import absolute_import  # pylint: disable=unused-variable

from coverage import CoverageException, Coverage

from deplytils.mocks import MockCoverage


class CoverageContext(object):
    """Context manager used to start and stop the coverage utility"""
    def __init__(self, coverage_args=(), coverage_kwargs=None, report=True,
                 report_type='report', report_args=(), mock_args=(),
                 mock_kwargs=None, report_kwargs=None, silent=True):
        """
        Manager used to capture and report python coverage with a
        single line (`with CoverageContext():`). Coverage constructor
        arguments, report type and report arguments can be specified
        by using the corresponding *_args and *_kwargs parameters.
        Additionally, reporting can be turned off completely.

        :param coverage_args: args for Coverage constructor - list like
        :param coverage_kwargs: kwargs for Coverage constructor - dict
        :param report: whether or not the report function should be
                generated - bool
        :param report_type: string representing the reporting method
                name of the Coverage object - str
        :param report_args: args for report method - list like
        :param report_kwargs: kwargs for report method - dict
        :param silent: if true, assures nothing is printed to
                the console when using `report` method - bool
        """
        if mock_kwargs is None:
            mock_kwargs = {}
        if report_kwargs is None:
            report_kwargs = {}
        if coverage_kwargs is None:
            coverage_kwargs = {}
        if silent:
            assert report_type == 'report'

            class PseudoFile(object):
                """Fake file writer"""
                def write(self, *args, **kwargs):
                    """Fake write method"""
                    pass

            report_kwargs['file'] = PseudoFile()

        self.coverage_args = coverage_args
        self.coverage_kwargs = coverage_kwargs
        self.mock_args = mock_args
        self.mock_kwargs = mock_kwargs
        self.should_report = report
        self.report_type = report_type
        self.report_args = report_args
        self.report_kwargs = report_kwargs

        self.coverage = CoverageContext.__get_coverage_instance(
            self.coverage_args, self.coverage_kwargs, self.mock_args,
            self.mock_kwargs)

        self.result = None

    __coverage_depth = 0

    @classmethod
    def __get_coverage_instance(cls, real_args, real_kwargs, mock_args,
                                mock_kwargs):
        """
        Gets the proper instance of coverage based on our current depth
        of coverage

        :param real_args: list like
        :param real_kwargs: dict like
        :param mock_args: list like
        :param mock_kwargs: dict like
        :return: instance of a Coverage object
        """
        if cls.__coverage_depth == 0:
            class_ = Coverage
            args = real_args
            kwargs = real_kwargs
        else:
            class_ = MockCoverage
            args = mock_args
            kwargs = mock_kwargs
        cls.__coverage_depth += 1
        return class_(*args, **kwargs)

    def __enter__(self):
        """Start coverage"""
        self.coverage.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop coverage and, if specified, report"""
        self.coverage.stop()
        CoverageContext.__exit()
        if self.should_report:
            report_method = getattr(self.coverage, self.report_type)
            self.result = report_method(
                *self.report_args, **self.report_kwargs)

    @classmethod
    def __exit(cls):
        cls.__coverage_depth -= 1


class StrictCoverage(CoverageContext):
    """
    A type of Coverage Context manager that throws errors on exit if
    the coverage does not meet the defined threshold
    """

    def __init__(self, threshold, *args, **kwargs):
        """
        Similar to CoverageContext. In addition to returning a report
        result, it will throw an error if the coverage threshold is
        not met

        :param threshold: Minimum coverage threshold
        :param args: see CoverageContext init
        :param report: Included for better error checking and
                parent class signature matching. Must be True in order
                for this class to work properly
        :param kwargs: see CoverageContext init
        """
        report = kwargs.setdefault('report', True)
        assert report, ('Failure to report will result in errors when '
                        'attempting to compare the reported result to the '
                        'specified threshold')
        super(StrictCoverage, self).__init__(*args, **kwargs)
        self.threshold = threshold

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        stops coverage and stores coverage data in self.result.
        Performs a compare and raises an error if the threshold
        is not met.

        :raises CoverageException: Coverage does not meet threshold
        """
        super(StrictCoverage, self).__exit__(exc_type, exc_val, exc_tb)
        if self.result < self.threshold:
            raise CoverageException(
                '{:0.2f}% does not meet {:0.2f}% threshold'.format(
                    self.result, self.threshold))
