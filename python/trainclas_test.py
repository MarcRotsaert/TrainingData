import polar_analyzer as pj
import nosql_adapter as mongodb
import time

path = r"C:\temp\polartest\polar-user-data-export"
mongad = mongodb.MongoPolar("polartest4", "polardb")
# result = mongad.morecomplexquery({"location": "baanbras"})


# for res in result:
#     session = pj.Trainses_mongo(path, rest)
#     # print(res)
#     if "trainingtype" in session.abstract:
#         print(session.abstract["trainingtype"])
#     else:
#         print("no type")
#     continue

# xx
if False:
    result = mongad.morecomplexquery({"trainingtype": {"$exists": False}})
    for res in result:
        session = pj.Trainses_mongo(res)
        # print(res)
        if "trainingtype" in session.abstract:
            print(session.abstract["trainingtype"])
        else:
            print("no type")
        # continue
        laps = session.return_laps()
        if laps != None:
            lapses = pj.RManualLapAnalyzer(laps)
            su = lapses.return_startuprunoutlaps()
            result = lapses.return_accelartion(ignorelaps=su[0] + su[1])
            print(result)
            print(sum(result))
            fname = session.abstract["fname"]
            ses = pj.Trainses(path, fname)
            samses = pj.SamAnalExtra(ses.samples)
            samses.plot("speed")
            time.sleep(1)


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
    session = pj.Trainses_mongo(res)
    # print(res)
    if "trainingtype" in session.abstract:
        print(session.abstract["trainingtype"])
    else:
        print("no type")
    # continue
    laps = session.return_laps()
    if laps != None:
        lapses = pj.RManualLapAnalyzer(laps)
        su = lapses.determine_startuprunoutlaps()
        result = lapses._determine_accelaration(ignorelaps=su[0] + su[1])
        print(result)
        print(sum(result))
        fname = session.abstract["fname"]
        print(fname)
        ses = pj.Trainses(path, fname)
        samses = pj.SamAnalExtra(ses.samples)
        samses.plot("speed")
        time.sleep(1)


xx
# for res in result:
#     session = pj.Trainses_mongo(res)
#     laps = session.return_laps()
#     if session.abstract["location"] == "baanbras":
#         if laps != None:
#             lapses = pj.RManualLapAnalyzer(laps)
#             print(session.abstract["fname"])
#             try:
#                 int_identity = lapses.identify_interval()
#                 mongad.updateOne(session.abstract["_id"], {"interval": int_identity})
#             except:
#                 pass
#             # print(lapses.identify_easyrun())
#             # print(lapses.identify_sprints())
#             print("__________________________")

result = mongad.returnDocs()
for res in result:
    session = pj.Trainses_mongo(res)
    laps = session.return_laps()
    if laps != None:
        lapses = pj.RManualLapAnalyzer(laps)
        print(session.abstract["fname"])
        print(session.abstract["location"])
        try:
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
        except:
            pass
    print("__________________________")
