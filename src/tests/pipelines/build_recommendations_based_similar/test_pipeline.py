"""
This is a boilerplate test file for pipeline 'build_recommendations_based_similar'
generated using Kedro 0.18.4.
Please add your pipeline tests here.

Kedro recommends using `pytest` framework, more info about it can be found
in the official documentation:
https://docs.pytest.org/en/latest/getting-started.html
"""

import pandas as pd

from multirec.pipelines.build_recommendations_based_similar.nodes import (
    get_recommendations,
)


def test_pipeline():
    input_indexed_df = pd.DataFrame(
        data={
            "Tags": [
                "Tag1, Tag2",
                "Tag1, Tag3",
                "Tag1, Tag2, Tag3",
            ]
        }
    )
    input_target_column = "Tags"

    output_recs = get_recommendations(input_target_column, input_indexed_df, top=2)

    assert output_recs["recommendations"].iloc[0] == [2, 1]
    assert output_recs["recommendations"].iloc[1] == [2, 0]
    assert output_recs["recommendations"].iloc[2] == [1, 0]
