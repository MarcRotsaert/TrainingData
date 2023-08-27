# Determine training type en set info in Mongo DB.
from typing import Generator

import polar_analyzer as pol_an
import nosql_adapter as mongodb
from polar_base import Base_training_classifier


class MongoRunningClassifier:
    def __init__(self, dbase: str, collection: str):
        self.mongo = mongodb.MongoPolar(dbase, collection)
        self.SPORT = "RUNNING"
        self.TRAININGTYPES = Base_training_classifier.TRAININGTYPES

    def print_trainingtypes(self) -> None:
        print(self.TRAININGTYPES)

    def _return_session(self, mongorecord) -> pol_an.Trainses_mongo:
        return pol_an.Trainses_mongo(mongorecord)

    def _generator_training(self) -> Generator:
        # yield all trainingen, from self.SPORT
        trainingen = self.mongo.simplequery("sport", self.SPORT)
        for training in trainingen:
            yield self._return_session(training)

    def set_roadrace(self) -> None:
        fnamerr = self._return_roadrace()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.roadrace": True})

    def _return_interval(self) -> list[str]:
        traingen = self._generator_training()
        intervaltr = {}
        for training in traingen:
            if training.laps is not None:
                lapses = pol_an.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
                    print(training.abstract["fname"])
                    print(lapses.laps["speed"])
                    print(len(lapses.laps))
                    try:
                        # TODO solution for empty laps (laps without information)
                        su_laps = lapses.determine_startuprunoutlaps()
                    except KeyError:
                        continue
                    x = lapses.identify_interval()
                    # s if x:
                    # print(lapses["fname"])
                    # print(training.abstract["fname"])
                    intervaltr.update({training.abstract["fname"]: x})
                    # except TypeError:
                    # print("Probabily no speed data ")
                    # time.sleep(1)
                    # pass
        return intervaltr

    def set_interval(self) -> None:
        trainingen = self._return_interval()
        for fname, descr in trainingen.items():
            cursor = self.mongo.simplequery("fname", fname)
            for res in cursor:
                objid = res["_id"]
                self.mongo.updateOne(
                    # objid, {"trainingtype.interval": trainingen[fname]}
                    objid,
                    {"trainingtype.interval": descr},
                )

    def _return_roadrace(self) -> list[str]:
        traingen = self._generator_training()
        race_alaps = []
        race_laps = []
        for training in traingen:
            if training.laps is not None:
                lapses = pol_an.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
                    try:
                        # TODO solution for empty laps (laps without information)
                        su_laps = lapses.determine_startuprunoutlaps()
                    except KeyError:
                        continue
                    ignorelaps = su_laps[0] + su_laps[1]
                    isroadrace = lapses.identify_roadrace(ignorelaps)
                    if isroadrace:
                        # print(lapses["fname"])
                        print(training.abstract["fname"])
                        race_laps.append(training.abstract["fname"])

            alapses = pol_an.RAutoLapAnalyzer(training.alaps)
            if len(alapses.laps) != 0:
                try:
                    # TODO solution for empty laps (laps without information)
                    # and clear this exception
                    isroadrace = alapses.identify_roadrace()
                except Exception:
                    continue  # print("not good!")
                if isroadrace:
                    print(training.abstract["fname"])
                    race_alaps.append(training.abstract["fname"])

        set1 = set(race_laps)
        set2 = set(race_alaps)
        return set1.union(set2)

    def _return_easyrun(self) -> list[str]:
        traingen = self._generator_training()
        easyrun = []

        for training in traingen:
            lapses = pol_an.RAutoLapAnalyzer(training.alaps)
            if len(lapses.laps) != 0:
                try:
                    if lapses.identify_easyrun():
                        easyrun.append(training.abstract["fname"])
                except KeyError:
                    continue
        return easyrun

    def set_easyrun(self) -> None:
        fnamerr = self._return_easyrun()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": True})

    def _return_sprint(self) -> list[str]:
        traingen = self._generator_training()
        sprint = []
        for training in traingen:
            if training.laps is not None:
                lapses = pol_an.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
                    if lapses.identify_sprints():
                        sprint.append(training.abstract["fname"])
        return sprint

    def set_sprint(self) -> list[str]:
        fnamerr = self._return_sprint()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.sprint": True})


if __name__ == "__main__":
    classif = MongoRunningClassifier("polartest4", "polar2014")

    classif.set_interval()
    road_races = classif.mongo.simplequery("trainingtype.interval", "interval, check1")
    for rr in road_races:
        print(rr)
    print("___________________________________________________")

    classif.set_roadrace()
    road_races = classif.mongo.simplequery("trainingtype.roadrace", True)
    for rr in road_races:
        print(rr)
    print("___________________________________________________")
    classif.set_easyrun()
    road_races = classif.mongo.simplequery("trainingtype.easyrun", True)
    for rr in road_races:
        print(rr)
    print("___________________________________________________")
    classif.set_sprint()
    road_races = classif.mongo.simplequery("trainingtype.sprint", True)
    for rr in road_races:
        print(rr)
