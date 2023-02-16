#!/usr/bin/python
import os
import glob

from nosql_adapter import MongoPolar
import polar_json as pj

mongad = MongoPolar("polartest", "polardb")
path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
files = glob.glob(os.path.join(path, "training-session-2015-*.json"))
pointcoll = []
for fi in files:
    # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
    filename = fi.split("\\")[-1]
    mongad.put_jsonresume(path, filename)
