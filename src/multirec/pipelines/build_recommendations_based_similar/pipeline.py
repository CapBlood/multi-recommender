"""
This is a boilerplate pipeline 'build_recommendations_based_similar'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from multirec.pipelines.build_recommendations_based_similar.nodes import (
    get_recommendations,
)


def create_pipeline(**kwargs) -> Pipeline:
    template_pipeline = pipeline(
        [
            node(
                func=get_recommendations,
                inputs=["params:target_column", "dataframe"],
                outputs="dataframe_with_recs",
            )
        ]
    )
    
    return template_pipeline
