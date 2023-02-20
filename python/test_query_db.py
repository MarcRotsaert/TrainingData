#!/usr/bin/python
import os
import glob

from nosql_adapter import MongoPolar
import polar_json as pj

mongad = MongoPolar("polartest2", "polardb")
path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
files = glob.glob(os.path.join(path, "training-session-2015-*.json"))
pointcoll = []

# items = mongad.returnDocs()
if False:
    items2 = mongad.simplequery("kiloCalories", 0)
    ses = pj.Trainses(None, None)
    ses.add_data(items2[20])
    print(ses.return_autolaps())
if True:
    items2 = mongad.simplequery("location", "baanbras")
    for it in items2:
        print("_________________")
        ses = pj.Trainses(None, None)
        ses.add_data_db(it)
        laps = ses.return_autolaps()
        if laps != None:
            for la in laps:
                print(la)

# mongad.morecomplexquery()

# for it in items:
#    print(it["location"])
