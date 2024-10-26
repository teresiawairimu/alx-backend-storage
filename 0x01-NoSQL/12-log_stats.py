#!/usr/bin/env python3
"""Provides stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_starts():
    """Function to print Nginx logs statistics

    Returns:
        Nginx logs statistics
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")
    status_filter = {"method": "GET", "path": "/status"}
    status_check = nginx_collection.count_documents(status_filter)
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
