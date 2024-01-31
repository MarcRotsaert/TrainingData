from training_classifier import MongoRunningClassifier, MongoIntervalTraining
from nosql_adapter import MongoQuery
import analyzer.garmin_analyzer as garan

dbase = "polartest"

collection = "garmin_2013"

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

if True:
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
