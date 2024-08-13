#!/usr/bin/env python3
""" mongdb with python3 """


def list_all(collection):
    """  lists all documents in a collection """
    return collection.find()
