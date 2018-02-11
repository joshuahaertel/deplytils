"""Test Extensions"""
import warnings
from unittest import TestCase

from deplytils.extensions.lint import ProjectLinter


# pylint: disable=unused-variable
class TestLintExtensions(TestCase):
    """Test Lint Extensions"""

    # pragma pylint: disable=missing-docstring,no-self-use
    def test_tests_with_no_path(self):
        """Actually testing our code base :)"""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings(
                "ignore", category=PendingDeprecationWarning)
            ProjectLinter().run()

    def test_deplytils_with_path(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings(
                "ignore", category=PendingDeprecationWarning)
            ProjectLinter('../deplytils', '.pylintrc').run()
