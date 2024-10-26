#!/usr/bin/env python3
"""Function to find all schoold having a specific topic"""

def schools_by_topic(mongo_collection, topic):
    """Returns a list of schools having a specific topic

    Args:
       mongo_collection: A pymongo collection object
       topic (str): the topic to search for

    Returns:
        list of documents matching the topic
    """
    return list(mongo_collection.find({"topics": topic}))
