
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='FinancialMining',  # Required
    version='0.2.8',  # Required
    description='financial data and mining',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/f496328mm/FinancialMining',  # Optional
    download_url = 'https://github.com/f496328mm/FinancialMining/tarball/v1.0',
    author='linsam',  # Optional
    author_email='samlin266118@gmail.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='financial, python',  # Optional
    packages=find_packages(exclude=['importlib', 'pymysql', 'pandas']),  # Required
    project_urls={  # Optional
        'Source': 'https://github.com/f496328mm/FinancialMining',
    },
)
