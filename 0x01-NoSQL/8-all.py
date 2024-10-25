#!/usr/bin/env python3
"""A module that lists all documents in a collection"""

def list_all(mongo_collection):
    """Lists all documents in a collection

    Parameter
        mongo_collection: pymongo collection object
    
    Returns:
        lists of documents or empty if none found
    """
    return list(mongo_collection.find())
