# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from os import path as os_path
from sys import path as sys_path
import sphinx_press_theme
import sphinx.ext.autodoc

sys_path.insert(0, os_path.abspath("../pandas_ta/"))
# sys_path.append(os_path.abspath("../pandas_ta/"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Pandas TA"
copyright = "2019+, Kevin Johnson"
author = "Kevin Johnson"
version = "0.3.14"
release = "beta"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# autodoc_mock_imports = ["pandas_ta"]

root_doc = "index"
source_suffix = [".rst", ".md"]

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.duration",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "autoapi.extension"
]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"
language = None

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


pygments_style = None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "press"
html_static_path = ["_static"]


napoleon_google_docstring = True

autoapi_type = "python"
autoapi_dirs = "../pandas_ta"