import os
from io import open

from setuptools import find_packages, setup

print(os.environ.get("CI_COMMIT_TAG", "0.0.0"))
_version = os.environ.get("CI_COMMIT_TAG", "0.0.1.dev2")

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def _process_requirements():
    packages = open("requirements.txt").read().strip().split("\n")
    requires = []
    for pkg in packages:
        if pkg.startswith("git+ssh"):
            return_code = os.system("pip install {}".format(pkg))
            assert return_code == 0, "error, status_code is: {}, exit!".format(
                return_code
            )
        else:
            requires.append(pkg)
    return requires


setup(
    name="finmind",  # Required
    version=_version,  # Required
    description="financial mining",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  # Optional (see note above)
    url="https://github.com/FinMind",  # Optional
    author="linsam",  # Optional
    author_email="finmind.tw@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Buil Tools",
        # "License :: OSI Approved :: MIT License",
        # "Programming Language :: Python :: 3.6",
    ],
    keywords="financial, python",  # Optional
    packages=find_packages(exclude=["*tests*"]),
    include_package_data=True,
    install_requires=_process_requirements(),
    project_urls={  # Optional
        "documentation": "https://finmind.github.io/",
        "Source": "https://github.com/FinMind/FinMind",
    },
)
