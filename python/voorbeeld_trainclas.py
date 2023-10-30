import time
from matplotlib import pyplot as pp
import random

from trainsession import Trainsession_mongo
import nosql_adapter as mongodb
import analyzer.polar_analyzer as pj


mongad = mongodb.MongoPolar("polartest4", "polar2014")
result = mongad.simplequery("location", "baanbras")

for res in result:
    session = Trainsession_mongo(res)
    if "trainingtype" in session.abstract:
        print(session.abstract["trainingtype"])
    else:
        print("no type")
    continue

if True:
    result = mongad.morecomplexquery({"trainingtype": {"$exists": False}})
    resultlist = list(result)
    for res in random.choices(resultlist, k=5):
        session = Trainsession_mongo(res)
        if "trainingtype" in session.abstract:
            print(session.abstract["trainingtype"])
        else:
            print("no type")
        # continue
        laps = session.return_laps()
        if laps is not None:
            lapses = session.RManualLapAnalyzer
            su = lapses.determine_startuprunoutlaps()
            result = lapses._determine_accelaration(ignorelaps=su[0] + su[1])
            print(result)
            print(sum(result))
            fname = session.abstract["fname"]
            samses = pj.Trainses_json(fname).SamAnalRunning
            samses.plot("speed")
            time.sleep(1)

if True:
    result = mongad.morecomplexquery(
        {
            "$and": [
                {"trainingtype.interval": {"$ne": "interval"}},
                {"trainingtype.interval": {"$ne": "interval, check"}},
                {"trainingtype.interval": {"$ne": "interval, check2"}},
                {"trainingtype.easyrun": {"$ne": True}},
                {"trainingtype.sprint": {"$ne": True}},
            ]
        }
    )
    for res in result:
        session = Trainsession_mongo(res)
        if "trainingtype" in session.abstract:
            print(session.abstract["trainingtype"])
        else:
            print("no type")
        laps = session.return_laps()
        if laps is not None:
            lapses = session.RManualLapAnalyzer
            su = lapses.determine_startuprunoutlaps()
            result = lapses._determine_accelaration(ignorelaps=su[0] + su[1])
            print(result)
            print(sum(result))
            fname = session.abstract["fname"]
            print(fname)
            ses = pj.Trainses_json(fname)
            samses = ses.SamAnalRunning
            samses.plot("speed")
            time.sleep(1)

    for res in result:
        session = Trainsession_mongo(res)
        laps = session.return_laps()
        if session.abstract["location"] == "baanbras":
            if laps is not None:
                lapses = session.RManualLapAnalyzer
                print(session.abstract["fname"])
                # try:
                int_identity = lapses.identify_interval()
                mongad.updateOne(session.abstract["_id"], {"interval": int_identity})
                # except:
                #     pass
                print(lapses.identify_easyrun())
                print(lapses.identify_sprints())
                print("__________________________")

result = mongad.returnDocs()
for res in result:
    session = Trainsession_mongo(res)
    laps = session.return_laps()
    if laps is not None:
        lapses = session.RManualLapAnalyzer
        print(session.abstract["fname"])
        print(session.abstract["location"])
        int_identity = lapses.identify_interval()
        print(int_identity)
        if int_identity == "interval" or int_identity == "interval, check":
            corcoef = lapses.compare_hr_sp()
            if corcoef > 0.7:
                hr_reliability = "good"
            elif corcoef > 0.35:
                hr_reliability = "doubt"
            else:
                hr_reliability = "bad"

            print(hr_reliability)
            mongad.updateOne(session.abstract["_id"], {"interval": int_identity})
            mongad.updateOne(
                session.abstract["_id"], {"hr_reliability": hr_reliability}
            )

            Ses = pj.Trainses_json(session.abstract["fname"])
            Samp = Ses.SamAnalRunning

            Samp.plot("speed")
            time.sleep(1)
            pp.close()
            if ("hr_reliability" in it) and (it["hr_reliability"] == "good"):
                Samp.plot("heartRate")
                time.sleep(1)
                pp.close()
    print("__________________________")
