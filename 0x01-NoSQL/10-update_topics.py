#!/usr/bin/env python3
"""Module that changes all topics of a school document based on the name"""

def update_topics(mongo_collection, name, topics):
    """Updates the list of topics document based on the name

    Args:
        mongo_collection: A pymongo collection object
        name (str): The school name to update
        topics (list of str): THe list of topics approached in school
    Returns:
        None
    """
    mongo_collection.update_many(
            {"name": name},
            {"$set": {"topics": topics}}
    )
