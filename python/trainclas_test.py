import polar_json as pj
import nosql_adapter as mongodb

mongad = mongodb.MongoPolar("polartest3", "polardb")
result = mongad.morecomplexquery({"location": "baanbras"})

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
