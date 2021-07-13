import sys
import logging
import urllib.parse
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import pandas as pd
from bson.objectid import ObjectId
import matplotlib.pyplot as plt
import os
import numpy as np

def get_client(url, username, password, needed_db):

    user = urllib.parse.quote_plus(username)
    pw = urllib.parse.quote_plus(password)
    client = MongoClient('mongodb://%s:%s@%s' % (user, pw, url),serverSelectionTimeoutMS=20000)
    while client is None:
        client = MongoClient('mongodb://%s:%s@%s' % (user, pw, url),serverSelectionTimeoutMS=20000)

    return client

my_client=get_client('192.168.0.110:27017','root','16883883Ftpisbst01','STADB')
cursor_result = my_client['STADB']['Data_statistics']
my_val = cursor_result.find({})
stdDF = pd.DataFrame.from_records(my_val, index=None)