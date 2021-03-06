# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../../photogrammetry_importer"))
sys.path.insert(0, os.path.abspath("../../.."))


# -- Project information -----------------------------------------------------

project = "Blender-Addon-Photgrammetry-Importer"
copyright = "2020, Sebastian Bullinger"
author = "Sebastian Bullinger"

# The full version, including alpha/beta/rc tags
release = "2.0.0"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

# https://github.com/readthedocs/sphinx_rtd_theme
import sphinx_rtd_theme

extensions = ["sphinx.ext.autodoc", "sphinx_rtd_theme"]

# Mock libraries that are missing at build time
autodoc_mock_imports = [
    "bpy",
    "bgl",
    "gpu",
    "mathutils",
    "gpu_extras",
    "bpy_extras",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["../../../photogrammetry_importer/ext"]

# -- Options for HTML output -------------------------------------------------

master_doc = "index"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Automatic API Documentation

# Option 1: sphinx-autoapi (recommended)
extensions.append("autoapi.extension")
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html
autoapi_type = "python"
autoapi_dirs = ["../../../photogrammetry_importer"]
autoapi_template_dir = ""
autoapi_options = [
    "members",
    # "inherited-members",
    "undoc-members",
    # "private-members",  # Something like _foo
    # "special-members",  # Something like __foo__
    # "imported-members",
    "show-inheritance",
    # "show-module-summary",  # Disables the table at the beginning of a module
]
autoapi_ignore = ["*migrations*", "*/ext/*"]
autoapi_root = "autoapi"
autoapi_add_toctree_entry = True
autoapi_keep_files = False

# Option 2: sphinx-apidoc
# https://github.com/readthedocs/readthedocs.org/issues/1139
# def run_apidoc(_):
#     from sphinx.ext.apidoc import main
#
#     sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
#     api_doc_odp = os.path.join(
#         os.path.abspath(os.path.dirname(__file__)), "apidoc"
#     )
#     photogrammetry_importer_idp = os.path.abspath(
#         "../../photogrammetry_importer"
#     )
#     if not os.path.isdir(api_doc_odp):
#         os.mkdir(api_doc_odp)
#     print("api_doc_odp", api_doc_odp)
#     print("photogrammetry_importer_idp", photogrammetry_importer_idp)
#     # This is the same as calling sphinx-apidoc from the command line
#     main(
#         [
#             "--module-first",
#             "--separate",
#             "--force",
#             "-o",
#             api_doc_odp,
#             photogrammetry_importer_idp,
#         ]
#     )
#
#
# def setup(app):
#     app.connect("builder-inited", run_apidoc)
