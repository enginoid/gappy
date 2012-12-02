from distutils.core import Command
from os.path import abspath, dirname
import os


class CheckCommand(Command):
    description = "Runs all tests that need to be fulfilled for release."
    user_options = []

    def initialize_options(self):
        self.dir = None

    def finalize_options(self):
        self.dir = dirname(abspath(__file__))

    def run(self):
        os.system('nosetests --with-cover {0}'.format(self.dir))
        os.system('pep8 --show-source --show-pep8 {0}'.format(self.dir))
