#!/usr/bin/python
import os
import glob

from nosql_adapter import MongoPolar
import polar_json as pj
import time
from matplotlib import pyplot as pp

mongad = MongoPolar("polartest3", "polardb")
path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
files = glob.glob(os.path.join(path, "training-session-2015-*.json"))
pointcoll = []

# items = mongad.returnDocs()
if False:
    items2 = mongad.simplequery("kiloCalories", 0)
    ses = pj.Trainses(None, None)
    ses.add_data(items2[20])
    print(ses.return_autolaps())

if False:
    items2 = mongad.simplequery("interval", "interval, check")

    for it in items2:
        fname = it["fname"]
        print("_________________")
        Ses = pj.Trainses(path, fname)
        Samp = pj.SamAnalExtra(Ses.samples)

        Samp.plot("speed")
        time.sleep(1)
        pp.close()
        if it["hr_reliability"] == "good":
            Samp.plot("heartRate")
            time.sleep(1)
            pp.close()


if True:
    items2 = mongad.simplequery("interval", "interval")

    for it in items2:
        fname = it["fname"]
        print("_________________")
        Ses = pj.Trainses(path, fname)
        Samp = pj.SamAnalExtra(Ses.samples)

        Samp.plot("speed")
        time.sleep(1)
        pp.close()
        if ("hr_reliability" in it) and (it["hr_reliability"] == "good"):
            Samp.plot("heartRate")
            time.sleep(1)
            pp.close()

if False:
    items2 = mongad.simplequery("interval", "interval")

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
