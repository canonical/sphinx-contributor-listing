"""Common utility functions for the sphinx-contributor-listing extension."""

from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file


def copy_custom_files(app: Sphinx, exc: Exception | None, filename: str) -> None:
    """Copy custom static files to the build output directory."""
    if not exc and app.builder.format == "html":
        staticfile = Path(app.builder.outdir) / "_static" / filename
        cssfile = Path(__file__).parent / "_static" / filename
        copy_asset_file(str(cssfile), str(staticfile))


def add_css(app: Sphinx, filename: str) -> None:
    """Register CSS file to be copied and added to the build."""
    app.connect(  # type: ignore[reportUnknownMemberType]
        "build-finished",
        lambda app, exc: copy_custom_files(app, exc, filename),  # type: ignore[reportUnknownLambdaType,reportUnknownArgumentType]
    )
    app.add_css_file(filename)


def add_js(app: Sphinx, filename: str) -> None:
    """Register JavaScript file to be copied and added to the build."""
    app.connect(  # type: ignore[reportUnknownMemberType]
        "build-finished",
        lambda app, exc: copy_custom_files(app, exc, filename),  # type: ignore[reportUnknownLambdaType,reportUnknownArgumentType]
    )
    app.add_js_file(filename)
