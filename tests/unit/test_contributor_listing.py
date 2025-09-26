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

"""Unit tests for sphinx-contributor-listing extension."""

# Ignore import organization warnings
# ruff: noqa: E402

from unittest.mock import MagicMock, Mock, patch

import pytest
from sphinx.application import Sphinx


class TestContributorListingSetup:
    """Test the extension setup function."""

    def test_setup_returns_metadata(self):
        """Test that setup returns proper extension metadata."""
        app_mock = Mock(spec=Sphinx)
        app_mock.connect = Mock()

        with patch("sphinx_contributor_listing.common.add_css") as mock_add_css, \
             patch("sphinx_contributor_listing.common.add_js") as mock_add_js:

            from sphinx_contributor_listing import setup
            result = setup(app_mock)

        assert result.get("parallel_read_safe", "") is True
        assert result.get("parallel_write_safe", "") is True

        # Verify the extension connects to the right event
        app_mock.connect.assert_called_once()
        connect_args = app_mock.connect.call_args[0]
        assert connect_args[0] == "html-page-context"

        # Verify CSS and JS are added
        mock_add_css.assert_called_once_with(app_mock, "contributors.css")
        mock_add_js.assert_called_once_with(app_mock, "contributors.js")


class TestContributorContextFunctions:
    """Test the context functions added by the extension."""

    def setup_method(self):
        """Set up test fixtures."""
        self.app_mock = Mock(spec=Sphinx)
        self.pagename = "test_page"
        self.templatename = "page.html"
        self.context = {}
        self.doctree = Mock()

    def test_get_contributors_no_config(self):
        """Test get_contributors_for_file when required config is missing."""
        # Missing display_contributors config
        from sphinx_contributor_listing.callback import add_contributor_context

        add_contributor_context(
            self.app_mock, self.pagename, self.templatename, self.context, self.doctree
        )

        result = self.context["get_contributors_for_file"]("test", ".md")
        assert result == []

    def test_get_contributors_disabled(self):
        """Test get_contributors_for_file when contributors display is disabled."""
        self.context["display_contributors"] = False
        self.context["github_folder"] = "/docs/"
        self.context["github_url"] = "https://github.com/example/repo"

        from sphinx_contributor_listing.callback import add_contributor_context

        add_contributor_context(
            self.app_mock, self.pagename, self.templatename, self.context, self.doctree
        )

        result = self.context["get_contributors_for_file"]("test", ".md")
        assert result == []

    @patch("sphinx_contributor_listing.callback.Repo")
    def test_get_contributors_invalid_repo(self, mock_repo_class):
        """Test get_contributors_for_file with invalid git repository."""
        from git import InvalidGitRepositoryError

        self.context["display_contributors"] = True
        self.context["github_folder"] = "/docs/"
        self.context["github_url"] = "https://github.com/example/repo"

        # Mock Repo to always raise InvalidGitRepositoryError for any path
        mock_repo_class.side_effect = InvalidGitRepositoryError

        from sphinx_contributor_listing.callback import add_contributor_context

        with patch("os.getcwd") as mock_getcwd:
            mock_getcwd.return_value = "/some/path/not/ending/with/docs"

            add_contributor_context(
                self.app_mock, self.pagename, self.templatename, self.context, self.doctree
            )

            result = self.context["get_contributors_for_file"]("test", ".md")
            # Should return empty list when repo can't be found
            assert result == []

    @patch("sphinx_contributor_listing.callback.Repo")
    def test_get_contributors_with_commits(self, mock_repo_class):
        """Test get_contributors_for_file with valid commits."""
        self.context["display_contributors"] = True
        self.context["github_folder"] = "/docs/"
        self.context["github_url"] = "https://github.com/example/repo"

        # Mock repository and commits
        mock_commit1 = Mock()
        mock_commit1.author.name = "Alice Developer"
        mock_commit1.co_authors = []
        mock_commit1.committed_date = 1234567890
        mock_commit1.hexsha = "abc123"

        mock_commit2 = Mock()
        mock_commit2.author.name = "Bob Developer"
        mock_commit2.co_authors = []
        mock_commit2.committed_date = 1234567900
        mock_commit2.hexsha = "def456"

        mock_repo = Mock()
        mock_repo.iter_commits.return_value = [mock_commit1, mock_commit2]
        mock_repo_class.return_value = mock_repo

        from sphinx_contributor_listing.callback import add_contributor_context

        add_contributor_context(
            self.app_mock, self.pagename, self.templatename, self.context, self.doctree
        )

        result = self.context["get_contributors_for_file"]("test", ".md")

        # Should return sorted list of contributors with links to their commits
        assert len(result) == 2
        assert ("Alice Developer", "https://github.com/example/repo/commit/abc123") in result
        assert ("Bob Developer", "https://github.com/example/repo/commit/def456") in result

    @patch("sphinx_contributor_listing.callback.Repo")
    def test_get_contributors_with_since_filter(self, mock_repo_class):
        """Test get_contributors_for_file with since filter."""
        self.context["display_contributors"] = True
        self.context["github_folder"] = "/docs/"
        self.context["github_url"] = "https://github.com/example/repo"
        self.context["display_contributors_since"] = "2024-01-01"

        mock_repo = Mock()
        mock_repo.iter_commits.return_value = []
        mock_repo_class.return_value = mock_repo

        from sphinx_contributor_listing.callback import add_contributor_context

        add_contributor_context(
            self.app_mock, self.pagename, self.templatename, self.context, self.doctree
        )

        self.context["get_contributors_for_file"]("test", ".md")

        # Should pass the since parameter to iter_commits
        mock_repo.iter_commits.assert_called_once_with(
            paths="docs/test.md",
            since="2024-01-01"
        )

    @patch("sphinx_contributor_listing.callback.Repo")
    def test_get_contributors_with_co_authors(self, mock_repo_class):
        """Test get_contributors_for_file with co-authors."""
        self.context["display_contributors"] = True
        self.context["github_folder"] = "/docs/"
        self.context["github_url"] = "https://github.com/example/repo"

        # Mock commit with co-authors
        mock_co_author = Mock()
        mock_co_author.name = "Co Author"

        mock_commit = Mock()
        mock_commit.author.name = "Main Author"
        mock_commit.co_authors = [mock_co_author]
        mock_commit.committed_date = 1234567890
        mock_commit.hexsha = "abc123"

        mock_repo = Mock()
        mock_repo.iter_commits.return_value = [mock_commit]
        mock_repo_class.return_value = mock_repo

        from sphinx_contributor_listing.callback import add_contributor_context

        add_contributor_context(
            self.app_mock, self.pagename, self.templatename, self.context, self.doctree
        )

        result = self.context["get_contributors_for_file"]("test", ".md")

        # Should include both main author and co-author
        assert len(result) == 2
        contributor_names = [name for name, _ in result]
        assert "Main Author" in contributor_names
        assert "Co Author" in contributor_names


# Import the module after defining the tests
import sphinx_contributor_listing