import os

from setuptools import setup

setup(version=os.environ.get("CI_COMMIT_TAG", "0.0.1.dev2"))
