#!/usr/bin/env python3
"""Inserts a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs

    Parameter:
         mongo_collection: pymongo collection object

    Return:
        _id: the new id of the document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
