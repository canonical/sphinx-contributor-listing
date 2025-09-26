# sphinx-contributor-listing

<!-- Answer elevator-pitch questions about the extension – What is it? What does it do? What
essential problem does it solve? -->

sphinx-contributor-listing adds contributor information to Sphinx documentation pages by extracting
Git commit history and displaying contributor names with links to their latest commits.

## Basic usage

<!-- Provide a few examples of the extension's most common use cases. Remember the Pareto
principle! -->

After installing and configuring the extension, contributor information becomes available in your
Sphinx templates through the `get_contributors_for_file` function. This function can be used in
custom templates to display contributor information for specific pages.

The extension automatically:
- Extracts commit history from the Git repository
- Identifies all contributors (including co-authors) for each file
- Provides links to the contributors' latest commits
- Supports filtering by date range

## Project setup

<!-- Provide the simplest way to install the extension. In most cases, this will
be via `pip`. -->

sphinx-contributor-listing can be installed with:

```bash
pip install sphinx-contributor-listing
```

After adding sphinx-contributor-listing to your Python project, update your Sphinx's conf.py file to
include sphinx-contributor-listing as one of its extensions:

```python
extensions = [
    "sphinx_contributor_listing"
]

# Configuration options
display_contributors = True  # Enable contributor display
github_folder = "/docs/"     # Path to documentation folder in repository
github_url = "https://github.com/your-org/your-repo"  # Base URL for commit links

# Optional: Filter commits by date
display_contributors_since = "2024-01-01"  # Only show contributors since this date
```

## Community and support

<!-- This is boilerplate. Replace the extension name and GitHub link. -->

You can report any issues or bugs on the project's [GitHub
repository](https://github.com/canonical/sphinx-contributor-listing).

sphinx-contributor-listing is covered by the [Ubuntu Code of
Conduct](https://ubuntu.com/community/ethos/code-of-conduct).

## License and copyright

<!-- Replace the extension name and, if necessary, the extension's license. -->

sphinx-contributor-listing is released under the [GPL-3.0 license](LICENSE).

© 2025 Canonical Ltd.
