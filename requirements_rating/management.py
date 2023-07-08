# -*- coding: utf-8 -*-

"""Console script for requirements-rating."""
import os
from pathlib import Path
from typing import Optional

import click

from requirements_rating._compat import USER_CACHE_DIR
from requirements_rating.dependencies import Dependencies
from requirements_rating.req_files import get_req_file_cls, REQ_FILE_CLASSES
from requirements_rating.results import Results


@click.group()
def cli():
    """Console script for requirements-rating."""
    pass


def common_options(function):
    function = click.option(
        "--cache-dir",
        envvar="PIP_CACHE_DIR",
        type=click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True),
        default=os.path.join(USER_CACHE_DIR, "wheels", "requirements-rating"),
        help="Use a custom cache dir.",
    )(function)
    function = click.option(
        "--index-url",
        # envvar="PIP_INDEX_URL",  # let pip discover
        # default="https://pypi.org/simple",
        help="Base URL of the Python Package Index (default https://pypi.org/simple).",
    )(function)
    function = click.option(
        "--extra-index-url",
        # envvar="PIP_EXTRA_INDEX_URL",  # let pip discover
        help="Extra URLs of package indexes to use in addition to --index-url.",
    )(function)
    return function


@cli.command()
@click.argument('file', type=click.Path(exists=True, dir_okay=False))
@click.option('--file-type', type=click.Choice(list(REQ_FILE_CLASSES.keys())), default=None)
@common_options
def analyze_file(file: str, file_type: Optional[str], cache_dir: str, index_url: str, extra_index_url: str):
    results = Results()
    file = Path(file)
    if file_type is None:
        req_file_cls = get_req_file_cls(file)
    else:
        req_file_cls = REQ_FILE_CLASSES[file_type]
    results.status.update(f"Read requirements file [bold green]{file}[/bold green]")
    dependencies = Dependencies(results, req_file_cls(file), cache_dir, index_url, extra_index_url)
    dependencies.get_global_rating_score()


@cli.command()
@click.argument('package_name')
@common_options
def analyze_package(package_name: str, cache_dir: str, index_url: str, extra_index_url: str):
    requirements = Dependencies(None, cache_dir, index_url, extra_index_url)
    package = requirements.get_package(package_name)
    score = package.rating.global_rating_score
    pass


if __name__ == '__main__':
    cli()
