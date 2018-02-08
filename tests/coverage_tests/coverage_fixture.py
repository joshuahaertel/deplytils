"""Fixture to test coverage context manager"""


# pragma pylint: disable=missing-docstring,unused-variable
# noinspection PyMissingOrEmptyDocstring,PyMethodMayBeStatic
class CoverageFixture(object):
    def __init__(self):
        self.covered = False

    def run(self):
        self.covered = True
