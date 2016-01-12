import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

with open("requirements.txt") as fhandler:
    install_requires = [
        line.strip()
        for line in fhandler.readlines()
    ]

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['tests']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='cheapflight',
    version='0.0.1.dev',
    url='http://github.com/mckelvin/cheap_flight/',
    license='BSD',
    author='mckelvin',
    author_email='mckelvin@noreply.github.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    scripts=[
        "manage.py"
    ],
    cmdclass={"test": PyTest},
    tests_require=[
        "pytest",
    ]
)
