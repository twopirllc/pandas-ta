# -*- coding: utf-8 -*-
from distutils.core import setup

long_description = "A Python 3 Pandas Extension of Technical Analysis Indicators"

setup(
    name = "pandas_ta",
    packages = ["pandas_ta"],
    version = "0.0.1a",
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
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
    ],
    # zip_safe=False,
)
