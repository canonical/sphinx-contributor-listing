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

"""Contains the callback functions for the sphinx-contributor-listing extension."""

import os
from typing import Any, Dict, List, Tuple, Optional

from git import Repo, InvalidGitRepositoryError
from sphinx.application import Sphinx
from sphinx.util import logging

logger = logging.getLogger(__name__)


def add_contributor_context(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Any,
) -> None:
    """Add contributor information to the page context."""

    def get_contributors_for_file(pagename: str, page_source_suffix: str) -> List[Tuple[str, str]]:
        """Get contributors for a specific file."""
        if (
            "display_contributors" not in context
            or "github_folder" not in context
            or "github_url" not in context
        ):
            return []

        if context["display_contributors"]:
            filename = f"{pagename}{page_source_suffix}"
            paths = context["github_folder"][1:] + filename

            try:
                repo = Repo(".")
            except InvalidGitRepositoryError:
                cwd = os.getcwd()
                ghfolder = context["github_folder"][:-1]
                if ghfolder and cwd.endswith(ghfolder):
                    try:
                        repo = Repo(cwd.rpartition(ghfolder)[0])
                    except InvalidGitRepositoryError:
                        logger.warning("The local Git repository could not be found.")
                        return []
                else:
                    logger.warning("The local Git repository could not be found.")
                    return []

            since: Optional[str] = None

            if (
                "display_contributors_since" in context
                and context["display_contributors_since"]
                and context["display_contributors_since"].strip()
            ):
                since = context["display_contributors_since"]

            try:
                commits = repo.iter_commits(paths=paths, since=since)
            except ValueError as e:
                logger.warning("Failed to iterate through the Git commits: %s", str(e))
                return []

            contributors_dict: Dict[str, Dict[str, Any]] = {}
            for commit in commits:
                contributors = [commit.author.name]
                for co_author in commit.co_authors:
                    contributors.append(co_author.name)
                for contributor in contributors:
                    if (
                        contributor not in contributors_dict
                        or commit.committed_date > contributors_dict[contributor]["date"]
                    ):
                        contributors_dict[contributor] = {
                            "date": commit.committed_date,
                            "sha": commit.hexsha,
                        }
            # github_page contains the link to the contributor's latest commit
            contributors_list = [
                (name, f"{context['github_url']}/commit/{data['sha']}")
                for name, data in contributors_dict.items()
            ]

            return sorted(contributors_list)

        else:
            return []

    context["get_contributors_for_file"] = get_contributors_for_file