"""Command line tools for manipulating a Kedro project.
Intended to be invoked via `kedro`."""
import click
from kedro.framework.cli.utils import (
    CONTEXT_SETTINGS,
)
from kedro.io import DataCatalog, MemoryDataSet
from kedro.extras.datasets.pandas import CSVDataSet
from kedro.runner import SequentialRunner
from kedro.framework.project import pipelines

from multirec.web.__main__ import run_web


@click.group(context_settings=CONTEXT_SETTINGS, name=__file__)
def cli():
    """Command line tools for manipulating a Kedro project."""


@cli.group()
def manage():
    """Консольная утилита для управления MultiRecommender."""

@manage.command()
@click.argument(
    'path',
    type=click.Path(exists=True, dir_okay=False)
)
@click.argument(
    'out',
    type=click.Path(exists=False, dir_okay=False)
)
@click.option(
    '--col',
    type=click.STRING,
    default='Tags',
    help='Наименование столбца для построения рекомендаций.'
)
def run(path, out, col):
    io = DataCatalog(
        {
            'dataframe': CSVDataSet(filepath=path),
            'dataframe_with_recs': CSVDataSet(filepath=out),
            'params:target_column': MemoryDataSet(col)
        }
    )
    
    default_pipeline = pipelines['__default__']

    SequentialRunner().run(default_pipeline, catalog=io)


@manage.command()
def web():
    run_web()
