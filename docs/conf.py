import os
import sys

project = "agrometeo-geopy"
author = "Martí Bosch"

__version__ = "0.1.3"
version = __version__
release = __version__

extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "myst_parser", "nbsphinx"]

autodoc_typehints = "description"
html_theme = "default"

# add module to path
sys.path.insert(0, os.path.abspath(".."))

# exclude patterns from sphinx-build
exclude_patterns = ["_build", "**.ipynb_checkpoints"]
