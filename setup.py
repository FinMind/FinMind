

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FinancialMining",
    version="0.0.1",
    author="linsam",
    author_email="samlin266118@gmail.com",
    description="financial data",
    long_description=long_description,
    url = 'https://github.com/f496328mm/FinancialMining',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

