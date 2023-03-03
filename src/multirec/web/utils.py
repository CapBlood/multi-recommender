import os

import streamlit as st
import pandas as pd
from kedro.io import DataCatalog, MemoryDataSet
from kedro.extras.datasets.pandas import CSVDataSet
from kedro.runner import SequentialRunner
from kedro.framework.project import pipelines
from kedro.framework.startup import bootstrap_project

from multirec.web.exceptions import TooMuchResults

@st.cache_data
def get_recs(input_csv, col):
    # Для того, чтобы инициализировать Kedro
    path = os.path.realpath(
        os.path.join(os.path.realpath(__file__), 
        "../../../../")
    )
    bootstrap_project(path)

    io = DataCatalog(
            {
                'dataframe': CSVDataSet(filepath=input_csv),
                'dataframe_with_recs': MemoryDataSet(),
                'params:target_column': MemoryDataSet(col)
            }
        )

        
    default_pipeline = pipelines['__default__']

    SequentialRunner().run(default_pipeline, catalog=io)

    return io.load('dataframe_with_recs')


@st.cache_data
def get_item_content(
        title: str, title_column_name: str,
        recs_column_name: str, df: pd.DataFrame) -> List[str]:
    
    title = title.lower()
    matches = df[df[title_column_name].str.lower() == title]
    if len(matches) == 0:
        matches = df[df[title_column_name].str.lower().str.contains(title)]
        if len(matches) == 0:
            # ...
            return

    if len(matches) > 1:
        raise TooMuchResults(
            "Too much results ({}). You must choose the only one:\n{}".format(
                len(matches), "\n".join(matches[title_column_name].to_list())
            )
        )
    
    item_series = matches.iloc[0]
    
    recs = item_series[recs_column_name]
    item_series_by_recs = df.loc[recs]

    return {
        'title': item_series['Name'],
        'desc': item_series['Russian_description'],
        'recs': item_series_by_recs['Name'].to_list()
    }
