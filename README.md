# sphinx-contributor-listing

sphinx-contributor-listing adds contributor information to Sphinx documentation pages by
extracting Git commit history and displaying contributor names with links to their
latest commits.

## Basic usage

After installing and configuring the extension, contributor information becomes
available in your Sphinx templates through the `get_contributors_for_file` function.
This function can be used in custom templates to display contributor information for
specific pages.

The extension automatically:

- Extracts commit history from the Git repository
- Identifies all contributors (including co-authors) for each file
- Provides links to the contributors' latest commits
- Supports filtering by date range

## Project setup

sphinx-contributor-listing can be installed with:

```bash
pip install sphinx-contributor-listing
```

After adding sphinx-contributor-listing to your Python project, update your Sphinx's
conf.py file to include sphinx-contributor-listing as one of its extensions:

```python
extensions = [
    "sphinx_contributor_listing"
]
```

Then, in your conf.py file, update `html_context` to include the following values:

```python
html_context = {
    # Required
    display_contributors = True  # Enable contributor display
    github_url = "https://github.com/your-org/your-repo"  # Base URL for commit links
    github_folder = "/docs/"     # Path to documentation folder in repository

    # Optional: Filter commits by date
    display_contributors_since = "2024-01-01"  # Only show contributors since this date
}
```

To list the contributors on each page, update your project's template to include the
`get_contributors_for_file` function. To display contributors in the page footer, you'd
update the `footer.html` file to include something akin to:

```html
  <div>
    {% if display_contributors and pagename and page_source_suffix %}
        {% set contributors = get_contributors_for_file(pagename, page_source_suffix) %}
        {% if contributors %}
          {% if contributors | length > 1 %}
              <a class="display-contributors">Thanks to the {{ contributors | length }} contributors!</a>
          {% else %}
              <a class="display-contributors">Thanks to our contributor!</a>
          {% endif %}
          <div id="overlay"></div>
          <ul class="all-contributors">
              {% for name, github_url in contributors %}
                  <li>
                      <a href="{{ github_url }}" class="contributor">{{ name }}</a>
                  </li>
              {% endfor %}
          </ul>
       {% endif %}
   {% endif %}
  </div>
```

For more information on templating in Sphinx, refer to
[Templating](https://www.sphinx-doc.org/en/master/development/html_themes/templating.html).

## Community and support

You can report any issues or bugs on the project's [GitHub
repository](https://github.com/canonical/sphinx-contributor-listing).

sphinx-contributor-listing is covered by the [Ubuntu Code of
Conduct](https://ubuntu.com/community/ethos/code-of-conduct).

## License and copyright

sphinx-contributor-listing is released under the [GPL-3.0 license](LICENSE).

© 2025 Canonical Ltd.
