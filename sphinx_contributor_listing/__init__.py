# This file is part of sphinx-contributor-listing.
#
# Copyright 2025 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License version 3, as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY
# QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

"""Contains the core elements of the sphinx-contributor-listing extension."""

from sphinx.application import Sphinx
from sphinx.util.typing import ExtensionMetadata

from sphinx_contributor_listing import common
from sphinx_contributor_listing.callback import add_contributor_context


try:
    from ._version import __version__
except ImportError:  # pragma: no cover
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version("sphinx-contributor-listing")
    except PackageNotFoundError:
        __version__ = "dev"


def setup(app: Sphinx) -> ExtensionMetadata:
    """Connect the callback function and add custom CSS and JS."""
    app.connect("html-page-context", add_contributor_context)
    common.add_css(app, "contributors.css")
    common.add_js(app, "contributors.js")

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


__all__ = ["__version__", "setup"]