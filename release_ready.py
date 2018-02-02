"""
Script to test release candidates. It performs linting as well as unit
tests with code coverage. If the linting is not perfect, all tests do
not pass, and there is not 100% coverage on project files (excluding
tests), the release candidate is not ready.
"""
import os
import subprocess
import unittest

import sys

from putils.contexts.coverage import StrictCoverage


class Checker(object):
    """
    Object to make sure unittests pass, the appropriate coverage is
    achieved, and everything passes linting.
    """
    def __init__(self):
        self._test_group_errors = 0
        try:
            os.remove('.coverage')
        except FileNotFoundError:
            pass

    def run(self):
        """Run all checks"""
        coverage_tests = self._start_coverage_tests()
        normal_tests = self._run_normal_tests()
        coverage_tests_output = self._output_coverage_tests(coverage_tests)
        self._validate_tests(coverage_tests, coverage_tests_output,
                             normal_tests)

    @staticmethod
    def _start_coverage_tests():
        """Start the process to test the CoverageContext"""
        args = 'coverage run -a -m unittest discover coverage_tests'
        coverage_tests = subprocess.Popen(
            args.split(' '), stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return coverage_tests

    @staticmethod
    def _run_normal_tests():
        """Run other/normal tests"""
        project_path = os.getenv('PYTHONPATH')
        config_file = os.path.join(project_path, '.ncoveragerc')
        with StrictCoverage(
                coverage_kwargs=dict(cover_pylib=False, branch=True,
                                     config_file=config_file),
                report_type='report', silent=True):
            tests = unittest.TestProgram(module=None, exit=False, argv=(
                'normal_tests', 'discover', 'tests'))
        return tests

    @staticmethod
    def _output_coverage_tests(coverage_tests):
        """Print coverage tests to stderr, as is expected"""
        coverage_tests.wait()
        coverage_tests_output = tuple(coverage_tests.stdout.readlines())
        for byte_line in coverage_tests_output:
            line = byte_line.decode('utf-8')
            print(line, file=sys.stderr)
        return coverage_tests_output

    def _validate_tests(self, coverage_tests, coverage_tests_output,
                        normal_tests):
        """Make sure all tests pass"""
        normal_test_results = normal_tests.result
        errors = normal_test_results.errors
        failures = normal_test_results.failures
        error_template = 'Encountered errors and/or failures in {} tests'

        self.__assert(normal_test_results.testsRun != 0,
                      'Did not run any test!')
        self.__assert(errors == [] and failures == [],
                      error_template.format('normal'))
        self.__assert(coverage_tests.returncode == 0 and
                      coverage_tests_output[-1] == b'OK\n',
                      error_template.format('coverage'))
        if self._test_group_errors != 0:
            print('Not all test groups passed!', file=sys.stderr)
            sys.exit(self._test_group_errors)
        print('Success! All tests passed!')

    def __assert(self, condition, error_message):
        """Log errors, but don't quit"""
        if not condition:
            print(error_message, file=sys.stderr)
            self._test_group_errors += 1


def main():
    """Run the checker"""
    checker = Checker()
    checker.run()


if __name__ == '__main__':
    main()
