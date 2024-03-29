from training_classifier import MongoRunningClassifier, MongoIntervalTraining

dbase = "polartest"
collections = []
years = range(2013, 2023)
collections = ["polar" + str(y) for y in years]
years = range(2011, 2014)
for year in range(2011, 2014):
    collections.append("garmin_" + str(year))

for collection in collections:
    classif = MongoRunningClassifier(dbase, collection)

    curs = classif.mongo.returnDocs()
    for training in curs:
        classif.mongo.deleteField(training["_id"], "trainingtype")
        classif.mongo.deleteField(training["_id"], "trainingdescription")

    classif.set_easyrun()
    easyrun, no_easyrun = classif.return_easyrun()
    road_races = classif.mongo.simplequery("trainingtype.easyrun", True)
    for rr in road_races:
        print(rr["fname"])
    print("___________________________________________________")
    classif.set_roadrace()
    road_races = classif.mongo.simplequery("trainingtype.roadrace", True)

    classif.set_interval()
    interval = classif.mongo.simplequery("trainingtype.interval", "interval")
    for train in interval:
        print(train)
        print("...........")

    classif.set_sprint()
    road_races = classif.mongo.simplequery("trainingtype.sprint", True)
    for rr in road_races:
        print(rr["fname"])

    print("___________________________________________________")
    interval = classif.mongo.simplequery("trainingtype.interval", "interval, check1")
    for rr in interval:
        print(rr["fname"])
    interval = classif.mongo.simplequery("trainingtype.interval", "interval, check2")
    for rr in interval:
        print(rr["fname"])
    interval = classif.mongo.simplequery("trainingtype.interval", "interval")
    for rr in interval:
        print(rr["fname"])

    for rr in road_races:
        print("___________________________________________________")
        print(rr["fname"])

    classif = MongoIntervalTraining(dbase, collection)
    classif.set_intervaldescription()
    classif.set_corrected_speed()

    print("Finish___________________________________________________")
