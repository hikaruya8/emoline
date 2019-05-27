import os, sys, logging, time, configparser
import pymongo
from pymongo import MongoClient, DESCENDING
import pandas as pd

# Const of database name
DICTIONARY_DB = "dictionaries"
PL_COLLECTION_NAME = "polarity"

# db接続情報は、`config.ini`に外だししておく
# --config.ini sample--------
# [mongo]
# id=**
# password=**
def get_db(db_name):
    # config = configparser.ConfigParser()
    # config.read( './config.ini')
    client = pymongo.MongoClient("mongodb+srv://hikaruya:neruson00@emoline-ubjn2.mongodb.net/test?retryWrites=true")
    db = client.test
    # client = MongoClient('localhost')
    # client['admin'].authenticate(config.get('mongo', 'id'), config.get('mongo', 'password'))
    # db = client[db_name]
    return db

# mongoDBのスキーマ
# ------------
# データベース名：dictionarries
# |- コレクション名：polarity
#    |- ドキュメント フォーマット： headword, score, ...
# （ドキュメント例： {headword="悪い", score=-1}, ...） 
def load_polarity_dict(collection_name):
    db = get_db(DICTIONARY_DB)
    cursor = db[collection_name].find()
    df = pd.DataFrame.from_dict(list(cursor)).astype(object)
    return df