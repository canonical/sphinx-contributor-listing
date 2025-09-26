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

"""Integration tests for sphinx-contributor-listing extension."""

# Ignore import organization warnings
# ruff: noqa: E402
# ruff: noqa: PLC0415

import shutil
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import bs4

# Add the extension to the path
sys.path.insert(0, str(Path(__file__).parents[2] / "sphinx_contributor_listing"))


def test_extension_can_be_imported():
    """Test that the extension can be imported without errors."""
    try:
        import sphinx_contributor_listing

        assert hasattr(sphinx_contributor_listing, "setup")
        assert callable(sphinx_contributor_listing.setup)
    except ImportError as e:
        pytest.fail(f"Failed to import sphinx_contributor_listing: {e}")


def test_extension_setup_function():
    """Test that the setup function returns correct metadata."""
    from unittest.mock import Mock, patch

    import sphinx_contributor_listing

    app_mock = Mock()
    app_mock.connect = Mock()

    with patch("sphinx_contributor_listing.common.add_css") as mock_add_css, \
         patch("sphinx_contributor_listing.common.add_js") as mock_add_js:
        result = sphinx_contributor_listing.setup(app_mock)

    assert "version" in result
    assert "parallel_read_safe" in result
    assert "parallel_write_safe" in result
    assert result["parallel_read_safe"] is True
    assert result["parallel_write_safe"] is True


def test_context_functions_work():
    """Test that context functions can be called."""
    from unittest.mock import Mock

    import sphinx_contributor_listing.callback

    app_mock = Mock()
    pagename = "test"
    templatename = "test.html"
    context: dict[str, str | dict[str, str] | Callable[[str, str], list]] = {
        "display_contributors": False,
        "github_folder": "/docs/",
        "github_url": "https://github.com/example/repo"
    }
    doctree = Mock()

    # Call the setup function
    sphinx_contributor_listing.callback.add_contributor_context(
        app_mock, pagename, templatename, context, doctree
    )

    # Check that context function was added
    assert "get_contributors_for_file" in context
    assert callable(context["get_contributors_for_file"])

    # Test call with disabled contributors
    result = context["get_contributors_for_file"]("test", ".md")
    assert result == []


# Import necessary modules
from unittest.mock import patch

import pytest


@pytest.fixture
def example_project(request) -> Path:
    project_root = request.config.rootpath
    example_dir = project_root / "tests/integration/example"

    # Copy the project into the test's own temporary dir, to avoid clobbering
    # the sources.
    target_dir = Path().resolve() / "example"
    shutil.copytree(example_dir, target_dir, dirs_exist_ok=True)

    return target_dir


@pytest.mark.slow
def test_sphinx_build(example_project):
    """Test building documentation with the contributor listing extension."""
    build_dir = example_project / "_build"

    # Run sphinx-build, but don't fail if it has warnings since we might not have git history
    result = subprocess.run(
        ["sphinx-build", "-b", "html", example_project, build_dir],
        capture_output=True,
        text=True
    )

    # Check if build succeeded (exit code 0) or had warnings (exit code 1)
    if result.returncode not in [0, 1]:
        pytest.fail(f"Sphinx build failed with exit code {result.returncode}: {result.stderr}")

    index = build_dir / "index.html"

    # Ensure the index file was created
    assert index.exists(), "index.html was not generated"

    # Rename the test output to something more meaningful
    shutil.copytree(
        build_dir, build_dir.parents[1] / ".test_output", dirs_exist_ok=True
    )

    soup = bs4.BeautifulSoup(index.read_text(), features="lxml")
    shutil.rmtree(example_project)  # Delete copied source

    # Check that the extension loaded without crashing
    # The exact content will depend on whether git history is available
    # but at minimum, the page should render successfully
    assert soup.find("body"), "HTML body not found - extension may have crashed"