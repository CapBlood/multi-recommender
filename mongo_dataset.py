import re
from typing import Any, Dict

import pandas as pd
from pymongo import MongoClient

from kedro.io import AbstractDataSet


class MongoDbDataset(AbstractDataSet[pd.DataFrame, pd.DataFrame]):
    def __init__(self, filepath: str, database: str, collection: str):
        protocol, path = re.split("://", filepath)
        self._protocol = protocol
        self._dbpath = path
        self._db = database
        self._collection = collection

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset."""
        return dict(filepath=self._dbpath, protocol=self._protocol)

    def _load(self) -> pd.DataFrame:
        client = MongoClient(self._dbpath)
        db = client[self._db]
        collection = db[self._collection]
        cursor = collection.find({})
        df = pd.json_normalize(cursor)
        for i in df.iterrows()[:10]:
            print(i)
            break

    def _save(self, data) -> None:
        pass
