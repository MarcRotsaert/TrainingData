import tomli
from nosql_adapter import MongoGarminfit, MongoForerunner, MongoPolar

# import analyzer.polar_analyzer as pol_an
# import analyzer.forerunner_analyzer as for_an
# import analyzer.garmin_analyzer as gar_an


# GET DATA FROM database
config = tomli.load(open("config.toml", "rb"))

path = config["garmin_fit"]["datapath"]

monggf = MongoGarminfit("testdatabase", "garminfit")
monggf.put_jsonresume("marcrotsaert_169919458.fit")

mongfr = MongoForerunner("testdatabase", "polar2004")
mongfr.showDocs()

path = config["forerunner_xml"]["datapath"]
mongfr.put_jsonresume("20050725-190632.xml")
print(mongfr.returnDocs())

mongad = MongoPolar("testdatabase", "polar2014")
mongad.showConnections()
coll = mongad.getCollection()
mongad.delete_duplicates()

if True:
    mongad.showConnections()
    coll = mongad.getCollection()
    docs = mongad.returnDocs()

if True:
    docs = mongad.return_docsrunning()
    for it in docs:
        print(it["fname"])

if True:
    #
    curs = mongad.simplequery("exportVersion", "1.6")
    curs = mongad.morecomplexquery({"latitude": {"$gt": 0}})
    curs = mongad.morecomplexquery({"physicalInformationSnapshot.sex": "MALE"})
    curs = mongad.morecomplexquery({"exercises[0].distance": 8960.0})
    curs = mongad.morecomplexquery({"exercises.speed.avg": {"$gt": 14}})
    curs = mongad.morecomplexquery(
        {
            "exercises.speed.avg": {"$gt": 14},
            "exercises.heartRate.avg": {"$gt": 140},
        }
    )
    curs = mongad.morecomplexquery(
        {"trainingtype.interval": "interval, check", "trainingtype.easyrun": True}
    )
    curs = mongad.simplequery("trainingtype.interval", "interval, check")
    # print(dir(curs))
    for c in curs:
        print(c["fname"])

if True:
    # remove fields
    items1 = mongad.getbyField("hr_reliability")
    for it in items1:
        mongad.deleteField(it["_id"], "hr_reliability")

    items2 = mongad.getbyField("hr_reliability")
    i = 0
    for it in items2:
        i += 1
    print(i)

# CHANGE DATABASE
if False:
    docs = mongad.returnDocs()
    ids = docs[0]["_id"]
    print(ids)
    if True:
        mongad.updateOne(ids, {"exportVersion": "69.0"})
    print("____________________________________")
