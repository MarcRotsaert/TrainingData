#!/usr/bin/python
import os
import glob

from nosql_adapter import MongoPolar
import polar_json as pj
import time
from matplotlib import pyplot as pp

path = r"C:\Users\marcr\Polar\Polar\data\polar-user-data-export"
files = glob.glob(os.path.join(path, "training-session-2015-*.json"))


mongad = MongoPolar("polartest3", "polardb")
pointcoll = []
# items = mongad.returnDocs()
# training-session-2015-06-03-263879174-463f62f9-4e7f-455a-9d42-fda0b0f237cc.json
# training-session-2015-06-08-263879330-1c199181-d38a-46ce-9c8b-c6eedff0d232.json, sprint
# training-session-2015-07-01-263876954-47f77cd5-a9ff-4008-988b-72281a367776.json
# training-session-2015-10-02-263860694-a0cc566f-63e0-4a22-ae42-e2b50b649e81.json, sprint
# training-session-2015-10-07-263860802-fb56334c-0b18-499a-91e7-2d3bd3b04d89.json
# training-session-2015-10-17-263860916-1b563b91-c4f4-4991-878c-5c1225f84b2c.json, sprint
result = mongad.simplequery("trainingtype.roadrace", True)
for res in result:
    print(res["trainingtype"])
# xx
result = mongad.morecomplexquery(
    {"$and": [{"trainingtype.sprint": True}, {"trainingtype.easyrun": True}]}
)
#         "trainingtype.interval": {"$ne": "interval"},
#         "trainingtype.interval": {"$ne": "interval, check"},
#         "trainingtype.roadrace": {"$ne": True},
#     }
# )
for res in result:
    print(res)

# xx
if True:
    fname = "training-session-2015-10-07-263860802-fb56334c-0b18-499a-91e7-2d3bd3b04d89.json"
    curs = mongad.simplequery("fname", fname)
    it = curs.next()
    print(it["trainingtype"])
    ses = pj.Trainses(path, fname)

    # xx
if True:
    items2 = mongad.simplequery("trainingtype.easyrun", True)
    # items2 = mongad.simplequery("interval", "interval, check")

    for it in items2:
        fname = it["fname"]
        print("_________________")
        print(fname)
        Ses = pj.Trainses(path, fname)
        Samp = pj.SamAnalExtra(Ses.samples)

        Samp.plot("speed")
        time.sleep(1)
        pp.close()

if True:
    items2 = mongad.getbyField("interval")
    for it in items2:
        print(it)
    # xx

if True:
    items2 = mongad.morecomplexquery({"trainingtype.interval": "interval"})

    for it in items2:
        fname = it["fname"]
        print("_________________")
        Ses = pj.Trainses(path, fname)
        Samp = pj.SamAnalExtra(Ses.samples)

        Samp.plot("speed")
        time.sleep(1)
        pp.close()
        # if ("hr_reliability" in it) and (it["hr_reliability"] == "good"):
        #     Samp.plot("heartRate")
        #     time.sleep(1)
        #     pp.close()

if True:
    items2 = mongad.simplequery("interval", "interval")

    for it in items2:
        print("_________________")
        ses = pj.Trainses(None, None)
        ses.add_data_db(it)
        laps = ses.return_autolaps()
        if laps != None:
            for la in laps:
                print(la)
