from training_classifier import MongoRunningClassifier, MongoIntervalTraining
from nosql_adapter import MongoQuery, MongoAdapter
import parsing.garminfit_parser as garpar
import parsing.forerunner_parser as forpar
import analyzer.forerunner_analyzer as forana
import analyzer.garmin_analyzer as garan

if True:
    dbase = "polartest"
    collection = "forerunner2007"
    mongo = MongoAdapter(dbase, collection)
    docs = mongo.returnDocs()
    for doc in docs:
        i = doc["_id"]
        fname = doc["fname"]
        loc = forana.Trainses_xml(fname).SamAnalRunning.determine_s_location()
        mongo.updateOne(i, {"location": loc})
        # print(loc)
        # if doc["laps"] is None:
        #     continue
        # if len(doc["laps"]) > 1:
        #     dist = doc["distance"]
        #     dur = doc["duration"]

        #     avgspeed = 3600 * dist / (1000 * dur)
        #     mongo.updateOne(i, {"speed.avg": avgspeed})
        #     print(i)


if False:
    dbase = "barriedb"
    collection = "garminfit"

    curs = MongoQuery(dbase, collection).simplequery("speed.avg", None)
    trainingen = list(curs)
    for train in trainingen:
        i = train["_id"]
        fname = train["fname"]
        abstr = garpar.Garminfit_parser(fname).extract_abstract()

        avgspeed = abstr["speed"]["avg"]
        maxspeed = abstr["speed"]["max"]
        # print({"speed": {"avg": avgspeed, "max": maxspeed}})
        MongoAdapter(dbase, collection).updateOne(
            i, {"speed": {"avg": avgspeed, "max": maxspeed}}
        )
        # print("yes")

if False:
    fileanal = garan.Trainses_fit("marcrotsaert_728350473.fit")

    ri, ru = fileanal.RAutoLapAnalyzer.determine_startuprunoutlaps()
    print(ri + ru)
    print(fileanal.RAutoLapAnalyzer.identify_roadrace(ri + ru))
    xx

if False:
    result = MongoQuery(dbase, collection).morecomplexquery(
        {"startTime": {"$regex": "^2013-09-01"}}
    )
    x = list(result)

    fname = x[0]["fname"]
    print(fname)
    xx
    # classif = MongoRunningClassifier(dbase, collection)

    fileanal = garan.Trainses_fit(fname)
    fileanal.RAutoLapAnalyzer.print_nrlaps()

    riru_laps = fileanal.RAutoLapAnalyzer.determine_startuprunoutlaps()
    print(fileanal.RAutoLapAnalyzer.identify_roadrace())

if False:
    classif = MongoRunningClassifier(dbase, collection)
    result_clas = classif.return_roadrace()
    # print(result_clas)
    curs = MongoQuery(dbase, collection).morecomplexquery(
        {"trainingtype.roadrace": True}
    )
    x = list(curs)
    result_dbase = [i["fname"] for i in x]

    print(len(result_clas))
    print(len(result_dbase))
    A = set(result_dbase)
    print(A.difference(result_clas))
