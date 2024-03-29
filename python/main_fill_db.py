import os
import glob

from nosql_adapter import MongoPolar, MongoForerunner
from nosql_adapter import MongoGarminfit, MongoQuery

import parsing.garminfit_parser as ga_pa

import tomli

config = tomli.load(open("config.toml", "rb"))
database = config["mongodb"]["database"]
# database = "testdb"


if False:
    path = config["polar_json"]["datapath"]
    # for year in [2014, 2015, 2017]:
    # for year in [2017]:
    for year in range(2013, 2022):
        mongad = MongoPolar(database, "polar" + str(year))
        files = glob.glob(
            os.path.join(path, "training-session-" + str(year) + "-*.json")
        )
        pointcoll = []
        for fi in files:
            # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
            filename = fi.split("\\")[-1]
            curs = MongoQuery(database, "polar" + str(year)).simplequery(
                "fname", filename
            )
            if len(list(curs)) == 0:
                mongad.put_jsonresume(filename)

if False:
    path = config["forerunner_xml"]["datapath"]
    for year in range(2004, 2008):
        files = glob.glob(os.path.join(path, str(year) + "*.xml"))
        pointcoll = []
        for fi in files:
            mongad = MongoForerunner(database, "forerunner" + str(year))
            filename = fi.split("\\")[-1]
            mongad.put_jsonresume(filename)


if False:
    path = config["garmin_fit"]["datapath"]
    # for year in range(2013, 2022):
    files = glob.glob(os.path.join(path, "*.fit"))
    mongad_2011 = MongoGarminfit(database, "garmin_2011")
    mongad_2012 = MongoGarminfit(database, "garmin_2012")
    mongad_2013 = MongoGarminfit(database, "garmin_2013")

    pointcoll = []
    for fi in files:
        # "training-session-2014-12-07-263916482-2cbe9312-6b71-4693-8519-a9a860a23cbc.json"
        try:
            abstract = ga_pa.Garminfit_parser(fi.split("\\")[-1]).extract_abstract()
            if abstract is not None:
                if abstract["startTime"][0:4] == "2011":
                    mongad = mongad_2011
                elif abstract["startTime"][0:4] == "2012":
                    mongad = mongad_2012
                elif abstract["startTime"][0:4] == "2013":
                    mongad = mongad_2013
                else:
                    print("no starttime in abstract")

                curs = MongoQuery(database, mongad.collection).simplequery(
                    "startTime", abstract["startTime"]
                )
                if len(list(curs)) == 0:
                    filename = fi.split("\\")[-1]
                    print(filename)
                    try:
                        mongad.put_jsonresume(filename)
                    except:
                        print(f"error in: {fi}")
                else:
                    print(f"duplicate: {fi}")
        except:
            print(f"major error in: {fi}")
