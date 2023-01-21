__all__ = [
    "MongoDbDataset"
]

from contextlib import suppress

with suppress(ImportError):
    from .mongo_dataset import MongoDbDataset
