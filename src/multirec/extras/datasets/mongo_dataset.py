import re
import json
from typing import Any, Dict

import pandas as pd
import numpy as np
from pymongo import MongoClient
from bson.codec_options import CodecOptions, TypeCodec
from bson.codec_options import TypeRegistry
from bson.int64 import Int64

from kedro.io import AbstractDataSet


class IntCodec(TypeCodec):
    python_type = np.int64    # the Python type acted upon by this type codec
    bson_type = Int64   # the BSON type acted upon by this type codec

    def transform_python(self, value: np.int64) -> Int64:
        return Int64(value)

    def transform_bson(self, value: Int64) -> int:
        return int(value)


class MongoDBDataset(AbstractDataSet[pd.DataFrame, pd.DataFrame]):
    def __init__(self, filepath: str, database: str, collection: str, filter_columns: list = []):
        protocol, path = re.split("://", filepath)
        self._protocol = protocol
        self._dbpath = path
        self._db = database
        self._collection = collection
        self._filter_columns = filter_columns

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=self._dbpath, protocol=self._protocol)

    def _load(self) -> pd.DataFrame:
        client = MongoClient(self._dbpath)
        db = client[self._db]
        collection = db[self._collection]
        cursor = collection.find({})
        df = pd.json_normalize(cursor)

        if self._filter_columns:
            df = df[self._filter_columns]

        return df

    def _save(self, data: pd.DataFrame) -> None:
        client = MongoClient(self._dbpath)
        db = client[self._db]

        codec_options = CodecOptions(
            type_registry=TypeRegistry([IntCodec()]))
        collection = db.get_collection(
            self._collection, codec_options=codec_options)

        if self._filter_columns:
            data = data[self._filter_columns]

        data.index = data.index.rename("_id")
        data = data.reset_index()
        data = data.to_dict(orient='records')

        for row in data:
            collection.update_one(
                {'_id': row['_id']}, {"$set": row}, upsert=True)
