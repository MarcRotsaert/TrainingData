#!/usr/bin/python
import os
import glob

from nosql_adapter import MongoPolar
import polar_json as pj
import tomli

config = tomli.load(open("config.toml", "rb"))
database = config['mongodb']['database']
path = config['polar_json']['datapath']
for year in range(2013, 2022):
    mongad = MongoPolar(database, "polar" + str(year))
    files = glob.glob(os.path.join(path, "training-session-" + str(year) + "-*.json"))
    pointcoll = []
    for fi in files:
        # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
        filename = fi.split("\\")[-1]
        mongad.put_jsonresume(path, filename)
