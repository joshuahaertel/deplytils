"""Linting utilities, primarily for deployment"""
import os

import re
from pylint.lint import Run


# pylint: disable=unused-variable
# noinspection SpellCheckingInspection
class ProjectLinter(object):
    """
    Lints all python files in a project. Note that python files must be
    in a directory that contains a __init__.py file, with the exception
    of the top directory in the project.
    """
    def __init__(self, project_path=None, rc_file=None, args=None, exit_=False,
                 reporter=None):
        """
        Runs pylint on an entire project

        :param project_path: absolute or relative path of project to
                lint
        :param rc_file: absolute or relative path of pylintrc file
        :param args: additional args for pylint in a list
        :param exit_: should exit after tests - bool
        :param reporter: reporter pylint argument
        """
        self.args = args if args else []
        if project_path is None:
            project_path = os.path.curdir
        self.project_path = os.path.abspath(project_path)
        self.rc_file = os.path.abspath(rc_file) if rc_file else ''
        self.files = []

        self.exit = exit_
        self.reporter = reporter

    def run(self):
        """Gathers files and runs the linter"""
        self._walk_dir(self.project_path)

        if not self.rc_file:
            self.args.append('--rcfile={}'.format(self.rc_file))

        self.args.extend(self.files)
        Run(self.args, reporter=self.reporter, exit=self.exit)

    def _walk_dir(self, path):
        """Gathers files"""
        for root, _, files in os.walk(path):
            if '__init__.py' not in files and root != self.project_path:
                continue

            for file in files:
                is_not_processable = re.search(r'local|.*(?<!\.py)$', file)
                if not is_not_processable:
                    self.files.append(os.path.join(root, file))
