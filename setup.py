# -*- coding: utf-8 -*-
from distutils.core import setup

long_description = "An easy to use Python 3 Pandas Extension with 130+ Technical Analysis Indicators. Can be called from a Pandas DataFrame or standalone like TA-Lib. Correlation tested with TA-Lib."

setup(
    name="pandas_ta",
    packages=[
        "pandas_ta",
        "pandas_ta.candles",
        "pandas_ta.cycles",
        "pandas_ta.momentum",
        "pandas_ta.overlap",
        "pandas_ta.performance",
        "pandas_ta.statistics",
        "pandas_ta.trend",
        "pandas_ta.utils",
        "pandas_ta.volatility",
        "pandas_ta.volume"
    ],
    version=".".join(("0", "2", "54b")),
    description=long_description,
    long_description=long_description,
    author="Kevin Johnson",
    author_email="appliedmathkj@gmail.com",
    url="https://github.com/twopirllc/pandas-ta",
    maintainer="Kevin Johnson",
    maintainer_email="appliedmathkj@gmail.com",
    # install_requires=["pandas"],
    download_url="https://github.com/twopirllc/pandas-ta.git",
    keywords=["technical analysis", "trading", "python3", "pandas"],
    license="The MIT License (MIT)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    package_data={
        "data": ["data/*.csv"],
    },
    install_requires=["pandas"],
    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        "dev": ["ta-lib", "jupyterlab", "sklearn", "statsmodels"],
        "test": ["ta-lib"],
    },
)
