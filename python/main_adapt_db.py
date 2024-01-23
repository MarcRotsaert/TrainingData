import os
import glob

from nosql_adapter import MongoPolar, MongoForerunner
from nosql_adapter import MongoGarminfit, MongoQuery

from analyzer import polar_analyzer, garmin_analyzer, forerunner_analyzer

# from trainsession import Trainsession_file
import tomli
from analyzer.sample_analyzer import SampleAnalyzerBasic

config = tomli.load(open("config.toml", "rb"))
database = config["mongodb"]["database"]
# database = "testdb"


if False:
    path = config["polar_json"]["datapath"]
    for year in range(2013, 2024):
        mongad = MongoPolar(database, "polar" + str(year))
        files = glob.glob(
            os.path.join(path, "training-session-" + str(year) + "-*.json")
        )

        for fi in files:
            # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
            filename = fi.split("\\")[-1]
            curs = MongoQuery(database, "polar" + str(year)).simplequery(
                "fname", filename
            )

            curslist = list(curs)
            if len(list(curslist)) != 0:
                # print(curslist)
                anal = polar_analyzer.Trainses_json(filename)
                location = anal.SamAnalRunning.determine_s_location()
                print(location)
                objid = curslist[0]["_id"]
                mongad.updateOne(objid, {"location": location})

if False:
    path = config["forerunner_xml"]["datapath"]
    for year in range(2004, 2008):
        files = glob.glob(os.path.join(path, str(year) + "*.xml"))
        pointcoll = []
        mongad = MongoForerunner(database, "forerunner" + str(year))

        for fi in files:
            filename = fi.split("\\")[-1]
            curs = MongoQuery(database, "forerunner" + str(year)).simplequery(
                "fname", filename
            )

            curslist = list(curs)
            if len(list(curslist)) != 0:
                anal = forerunner_analyzer.Trainses_xml(filename)
                location = anal.SamAnalRunning.determine_s_location()
                print(location)
                objid = curslist[0]["_id"]
                mongad.updateOne(objid, {"location": location})


if True:
    path = config["garmin_fit"]["datapath"]
    # for year in range(2013, 2022):
    files = glob.glob(os.path.join(path, "*.fit"))
    mongad = MongoGarminfit(database, "garminfit")

    for fi in files:
        filename = fi.split("\\")[-1]
        curs = MongoQuery(database, "garminfit").simplequery("fname", filename)

        curslist = list(curs)
        if len(list(curslist)) != 0:
            anal = garmin_analyzer.Trainses_fit(filename)
            location = anal.SamAnalRunning.determine_s_location()
            objid = curslist[0]["_id"]
            mongad.updateOne(objid, {"location": location})
