"""
This is a boilerplate pipeline 'drop_nan_column'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import drop_nan_column

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=drop_nan_column,
            inputs=["dataframe", "params:target_column"],
            outputs="dataframe_without_nan",
        )
    ])
