"""Project pipelines."""
from typing import Dict

from kedro.framework.project import find_pipelines
from kedro.pipeline.modular_pipeline import pipeline
from kedro.pipeline import Pipeline

from multirec.pipelines.build_recommendations_based_similar.pipeline import create_pipeline as build_create_pipeline
from multirec.pipelines.drop_nan_column.pipeline import create_pipeline as drop_nan_create_pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = dict()
    
    preprocess_pipeline = drop_nan_create_pipeline()
    build_recs_pipeline = pipeline(
        pipe=build_create_pipeline(),
        inputs={
            "dataframe": "dataframe_without_nan"
        }
    )

    pipelines["__default__"] = preprocess_pipeline + build_recs_pipeline

    # build_rec_pipe = create_pipeline()
    # pipelines["add_recommendations_to_mongo"] = build_rec_pipe
    # pipelines["update_recommendations_to_mongo"] = pipeline(
    #     pipe=build_rec_pipe,
    #     inputs={"dataframe": "mongo_dataframe"}
    # )

    return pipelines
