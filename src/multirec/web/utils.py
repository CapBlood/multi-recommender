from typing import List

import streamlit as st
import pandas as pd

from multirec.web.exceptions import TooMuchResults, ItemNotFound, IncorrectCsvStructure
from multirec.web.constants import CSV_FIELDS


@st.cache_data
def get_recs(input_csv, mapping=None):
    df = pd.read_csv(
        input_csv
    )

    if mapping is not None:
        for map_name in mapping.values():
            if map_name in df.columns:
                df = df.drop(columns=[map_name])

        df = df.rename(columns=mapping)

    for csv_field in CSV_FIELDS:
        if csv_field not in df.columns:
            raise IncorrectCsvStructure(
                "Incorrect structure in {}: field {} doesn't exist".format(
                    input_csv, csv_field)
            )
        
    df['Recommendations'] = df['Recommendations'].apply(
        lambda x: list(map(int, x.strip("[]").split(", ")))
    )

    return df


@st.cache_data
def get_item_content(
        title: str, df: pd.DataFrame) -> List[str]:

    title = title.lower()
    matches = df[df['Name'].str.lower() == title]
    if len(matches) == 0:
        matches = df[df['Name'].str.lower().str.contains(title)]

    if len(matches) == 0:
        raise ItemNotFound("'{}' doesn't exist".format(title))

    if len(matches) > 1:
        raise TooMuchResults(
            "Too much results ({}). You must choose the only one:\n{}".format(
                len(matches), "\n".join(matches['Name'].to_list())
            )
        )
    
    item_series = matches.iloc[0]
    
    recs = item_series["Recommendations"]
    item_series_by_recs = df.loc[recs]

    return {
        'title': item_series['Name'],
        'desc': item_series['Description'],
        'url': item_series['Url'],
        'tags': item_series['Tags'],
        'recs': item_series_by_recs['Name'].to_list()
    }
