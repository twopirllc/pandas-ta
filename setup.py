# -*- coding: utf-8 -*-
from distutils.core import setup

long_description = "An easy to use Python 3 Pandas Extension of Technical Analysis Indicators"

setup(
    name = "pandas_ta",
    packages = ["pandas_ta"],
    version = "0.1.14a",
    description=long_description,
    long_description=long_description,
    author = "Kevin Johnson",
    author_email = "appliedmathkj@gmail.com",
    url = "https://github.com/twopirllc/pandas-ta",
    maintainer="Kevin Johnson",
    maintainer_email="appliedmathkj@gmail.com",
    # install_requires=['numpy','pandas'],
    download_url = "https://github.com/twopirllc/pandas-ta.git",
    keywords = ['technical analysis', 'python3', 'pandas'],
    license="The MIT License (MIT)",
    classifiers = [
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    package_data={
        'data': ['data/*.csv'],
    },
    install_requires=['pandas'],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['ta-lib', 'jupyterlab'],
        'test': ['ta-lib'],
    },
)
