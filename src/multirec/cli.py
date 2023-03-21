"""Command line tools for manipulating a Kedro project.
Intended to be invoked via `kedro`."""
import subprocess
import os

import click
from kedro.framework.cli.utils import (
    CONTEXT_SETTINGS,
)
from kedro.io import DataCatalog, MemoryDataSet
from kedro.extras.datasets.pandas import CSVDataSet
from kedro.runner import SequentialRunner
from kedro.framework.project import pipelines


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
@click.option(
    '--size',
    type=click.INT,
    default=10,
    help='Количество получаемых рекомендаций для каждой строки.'
)
@click.option(
    '--index',
    type=click.STRING,
    default=None,
    help='Наименование столбца индексов.'
)
def run(path, out, col, size, index):
    io = DataCatalog(
        {
            'dataframe': CSVDataSet(
                filepath=path, 
                load_args={
                    'index_col': index
                }
            ),
            'dataframe_with_recs': CSVDataSet(
                filepath=out,
                save_args={'index': True}
            ),
            'params:size': MemoryDataSet(size),
            'params:target_column': MemoryDataSet(col)
        }
    )
    
    default_pipeline = pipelines['__default__']

    SequentialRunner().run(default_pipeline, catalog=io)


@manage.command()
@click.argument(
    'csv_path',
    type=click.Path(exists=True, dir_okay=False)
)
@click.option(
    '--mappings',
    type=click.STRING
)
@click.option(
    '--index',
    type=click.STRING,
    default=None,
    help='Наименование столбца индексов.'
)
def web(csv_path, mappings, index):
    env = dict()
    if mappings:
        env['MAPPINGS'] = mappings
    if index:
        env['INDEX'] = index

    os.environ.update(env)
    subprocess.run([
        "streamlit", "run", "src/multirec/web/app.py",
        csv_path
    ])
