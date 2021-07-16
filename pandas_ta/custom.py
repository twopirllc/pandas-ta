# -*- coding: utf-8 -*-

import os
import sys
from os.path import abspath, join, exists, basename, splitext
from glob import glob
import importlib
import pandas_ta
import pandas as pd
from pandas_ta import AnalysisIndicators

def create_dir(dir_path, create_categories=True, verbose=True):
    """ 
    Helper function to setup a suitable folder structure for working with 
    custom indicators.

    Args:
        dir_path (str): Full path to where you want your indicator tree
        create_categories (bool): If True create category sub-folders
        verbose (bool): If True verbose output of results
    """

    # ensure that the passed directory exists / is readable
    if not exists(dir_path):
        os.makedirs(dir_path)
        if verbose:
            print(f"[i] Created main directory '{dir_path}'.")

    # list the contents of the directory
    dirs = glob(abspath(join(dir_path, '*')))

    # optionally add any missing category subdirectories
    if create_categories:
        for sd in [*pandas_ta.Category]:
            d = abspath(join(dir_path, sd))
            if not exists(d):
                os.makedirs(d)
                if verbose:
                    dirname = basename(d)
                    print(f"[i] Created an empty sub-directory '{dirname}'.")

def import_dir(dir_path, verbose=True):

    # ensure that the passed directory exists / is readable
    if not exists(dir_path):
        print(f"[X] Unable to read the directory '{dir_path}'.")
        return

    # list the contents of the directory
    dirs = glob(abspath(join(dir_path, '*')))

    # traverse full directory, importing all modules found there
    for d in dirs:
        dirname = basename(d)

        # only look in directories which are valid pandas_ta categories
        if dirname not in [*pandas_ta.Category]:
            if verbose:
                print(f"[i] Skipping the sub-directory '{dirname}' since it's not a valid pandas_ta category.")
            continue

        # for each module found in that category (directory)...
        for module in glob(abspath(join(dir_path, dirname, '*.py'))):
            module = splitext(basename(module))[0]

            # ensure that the supplied path is included in our python path
            if d not in sys.path:
                sys.path.append(d) 

            # import the module and add it to the correct category
            importlib.import_module(module, d)
            pandas_ta.Category[dirname].append(module)

            if verbose:
                print(f"[i] Successfully imported the custom indicator '{module}' into category '{dirname}'.")

import_dir.__doc__ = \
"""
Import a directory of custom indicators into pandas_ta

Args:
    dir_path (str): Full path to your indicator tree
    verbose (bool): If True verbose output of results

This method allows you to experiment and develop your own technical analysis
indicators in a separate local directory of your choice but use them seamlessly 
together with the existing pandas_ta functions just like if they were part of 
pandas_ta.

If you at some late point would like to push them into the pandas_ta library
you can do so very easily by following the step by step instruction here
https://github.com/twopirllc/pandas-ta/issues/264.

Let's get started!

1. Loading the 'ta' module:
>>> import pandas as pd
>>> import pandas_ta as ta

2. Create an empty directory on your machine where you want to work with your
indicators. Invoke pandas_ta.custom.import_dir once to pre-populate it with 
sub-folders for all available indicator categories, e.g.:

>>> import os
>>> from os.path import abspath, join, expanduser
>>> from pandas_ta.custom import create_dir, import_dir
>>> my_dir = abspath(join(expanduser("~"), "my_indicators"))
>>> create_dir(my_dir)

3. You can now create your own custom indicator e.g. by copying existing 
ones from pandas_ta core module and modifying them. Each custom indicator 
should have a unique name and have both a function and a method defined
within the module. In essence these modules should look exactly like the
standard indicators available in categories under the pandas_ta-folder.

The only difference will be an addition of a matching class method that
will be imported dynamically to the AnalysisIndicators class and a
call to the utility function that binds the indicator name to pandas_ta.

For an example of the correct structure, look at the example ni.py in the 
examples folder.

The ni.py indicator is a trend indicator so therefoe we drop it into the 
sub-folder named trend. Thus we have a folder structure like this:

~/my_indicators/
│
├── candles/
.
.
└── trend/
.      └── ni.py
.
└── volume/

4. We can now dynamically load all our custom indicators located in our
designated indicators directory like this:

>>> import_dir(my_dir)

If your custom indicator loaded succesfully then it should behave exactly
like all other native indicators in pandas_ta, including help functions.
"""

def bind(function_name, function, method):
    """ 
    Helper function to bind the function and class method defined in a custom
    indicator module to the active pandas_ta instance. It is supposed to be
    invoked last in all custom indicator modules.

    Args:
        function_name (str): The name of the indicator within pandas_ta
        function (fcn): The indicator function
        method (fcn): The class method corresponding to the passed function
    """
    setattr(pandas_ta, function_name, function)
    setattr(AnalysisIndicators, function_name, method)