import os
from io import open

from setuptools import setup, find_packages

print(os.environ.get("CI_COMMIT_TAG", "0.0.0"))
_version = os.environ.get("CI_COMMIT_TAG", "0.0.1.dev2")

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "ta==0.5.25",
    "requests==2.23.0",
    "importlib_metadata==1.6.1",
    "matplotlib==3.2.1",
    "pandas==1.1.5",
    "pydantic==1.6.1",
]

setup(
    name="FinMind",  # Required
    version=_version,  # Required
    description="financial mining",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/linsamtw",  # Optional
    author="linsam",  # Optional
    author_email="samlin266118@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Buil Tools",
        # "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 3.6",
    ],
    keywords="financial, python",  # Optional
    packages=find_packages(exclude=["importlib", "ta"]),
    install_requires=requirements,
    project_urls={  # Optional
        "documentation": "https://linsamtw.github.io/FinMindDoc/",
        "Source": "https://github.com/linsamtw/FinMind",
    },
)
