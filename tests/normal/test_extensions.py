"""Test Extensions"""
import warnings
from unittest import TestCase

from putils.extensions.lint import ProjectLinter


# pylint: disable=unused-variable
class TestLintExtensions(TestCase):
    """Test Lint Extensions"""

    # pragma pylint: disable=missing-docstring,no-self-use
    def test_putils(self):
        """Actually testing our code base :)"""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings(
                "ignore", category=PendingDeprecationWarning)
            ProjectLinter().run()

    def test_path(self):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings(
                "ignore", category=PendingDeprecationWarning)
            ProjectLinter('normal', '.pylintrc').run()
