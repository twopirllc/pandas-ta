# -*- coding: utf-8 -*-
from distutils.core import setup

long_description = "Pandas Technical Analysis, Pandas TA, is a free, Open Source, and easy to use Technical Analysis library with a Pandas DataFrame Extension. It has over 200 indicators, utility functions and TA Lib Candlestick Patterns. Beyond TA feature generation, it has a flat library structure, it's own DataFrame Extension (called 'ta'), Custom Indicator Studies and Independent Custom Directory."

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
        "pandas_ta.transform",
        "pandas_ta.trend",
        "pandas_ta.utils",
        "pandas_ta.utils.data",
        "pandas_ta.volatility",
        "pandas_ta.volume"
    ],
    version=".".join(("0", "3", "79b")),
    description=long_description,
    long_description=long_description,
    author="Kevin Johnson",
    author_email="appliedmathkj@gmail.com",
    url="https://github.com/twopirllc/pandas-ta",
    maintainer="Kevin Johnson",
    maintainer_email="appliedmathkj@gmail.com",
    download_url="https://github.com/twopirllc/pandas-ta.git",
    keywords=[
        "technical analysis", "trading", "backtest", "trading bot",
        "features",
        "pandas", "numpy", "vectorbt", "yfinance", "polygon",
        "python3"
    ],
    license="The MIT License (MIT)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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
        "pandas_ta": ["py.typed"],
        "data": ["data/*.csv"],
    },
    install_requires=["pandas"],
    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[full,test]     # locally
    # $ pip install -U pandas_ta[full]  # pip
    extras_require={
        "full": [
            "alphaVantage-api", "matplotlib", "mplfinance", "numba", "polygon"
            "python-dotenv", "scipy", "sklearn", "statsmodels", "stochastic",
            "ta-lib", "tqdm", "vectorbt", "yfinance",
        ],
        "test": [
            "pytest==7.1.2",
            "pandas_datareader==0.10.0",
            "ta-lib"
        ],
    },
)
