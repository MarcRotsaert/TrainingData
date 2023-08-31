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
        fnamerr = self.return_roadrace()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.roadrace": True})

    def return_roadrace(self) -> list[str]:
        traingen = self._generator_training()
        race_laps = []
        race_alaps = []

        for training in traingen:
            if training.laps is not None:
                result1 = self._return_roadrace_laps(training)
                if result1 is not False:
                    race_laps.append(result1)

            result2 = self._return_roadrace_alaps(training)
            if result2 is not False:
                race_alaps.append(result2)

        set1 = set(race_laps)
        set2 = set(race_alaps)
        return set1.union(set2)

    def _return_roadrace_laps(self, training):
        lapses = pol_an.RManualLapAnalyzer(training.laps)
        su_laps = lapses.determine_startuprunoutlaps()
        if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
            if su_laps is None:
                return False
            ignorelaps = su_laps[0] + su_laps[1]
            isroadrace = lapses.identify_roadrace(ignorelaps)
            if isroadrace:
                print(training.abstract["fname"])
                return training.abstract["fname"]
            else:
                return False

    def _return_roadrace_alaps(self, training: dict) -> str or False:
        alapses = pol_an.RAutoLapAnalyzer(training.alaps)
        if len(alapses.laps) == 0:
            return False

        isroadrace = alapses.identify_roadrace()
        if isroadrace:
            print(training.abstract["fname"])
            return training.abstract["fname"]
        else:
            return False

    def set_interval(self) -> None:
        trainingen = self.return_interval()
        for fname, descr in trainingen.items():
            cursor = self.mongo.simplequery("fname", fname)
            for res in cursor:
                objid = res["_id"]
                self.mongo.updateOne(
                    objid,
                    {"trainingtype.interval": descr},
                )

    def return_interval(self) -> dict:
        traingen = self._generator_training()
        intervaltr = {}
        for training in traingen:
            if training.laps is not None:
                lapses = pol_an.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
                    result = lapses.identify_interval()
                    intervaltr.update({training.abstract["fname"]: result})
        return intervaltr

    def set_easyrun(self) -> None:
        easyrun, no_easyrun = self.return_easyrun()
        for fname in easyrun:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": True})
        for fname in no_easyrun:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.easyrun": False})

    def return_easyrun(self) -> list[str]:
        traingen = self._generator_training()
        easyrun = []
        no_easyrun = []

        for training in traingen:
            if (
                training.abstract["fname"]
                == "training-session-2014-04-11-263909204-dcdf0fcf-b3d8-4f81-8920-75352b184a6c.json"
            ):
                print("x")
                # xx
            lapses = pol_an.RManualLapAnalyzer(training.laps)
            if len(lapses.laps) == 0:
                continue
            if lapses.identify_easyrun():
                easyrun.append(training.abstract["fname"])
            else:
                no_easyrun.append(training.abstract["fname"])
        return easyrun, no_easyrun

    def set_sprint(self) -> list[str]:
        fnamerr = self.return_sprint()
        for fname in fnamerr:
            result = self.mongo.simplequery("fname", fname)
            for res in result:
                objid = res["_id"]
                self.mongo.updateOne(objid, {"trainingtype.sprint": True})

    def return_sprint(self) -> list[str]:
        traingen = self._generator_training()
        sprint = []
        for training in traingen:
            if training.laps is not None:
                lapses = pol_an.RManualLapAnalyzer(training.laps)
                if (len(lapses.laps) != 0) & (lapses.laps["speed"] is not None):
                    if lapses.identify_sprints():
                        sprint.append(training.abstract["fname"])
        return sprint


if __name__ == "__main__":
    classif = MongoRunningClassifier("polartest4", "polar2014")

    easyrun, no_easyrun = classif.return_easyrun()
    classif.set_easyrun()
    road_races = classif.mongo.simplequery("trainingtype.easyrun", True)
    for rr in road_races:
        print(rr["fname"])
    print("___________________________________________________")
    xx
    classif.set_sprint()
    road_races = classif.mongo.simplequery("trainingtype.sprint", True)
    for rr in road_races:
        print(rr["fname"])

    print("___________________________________________________")
    classif.set_interval()
    interval = classif.mongo.simplequery("trainingtype.interval", "interval, check1")
    for rr in interval:
        print(rr["fname"])
    interval = classif.mongo.simplequery("trainingtype.interval", "interval, check2")
    for rr in interval:
        print(rr["fname"])
    interval = classif.mongo.simplequery("trainingtype.interval", "interval")
    for rr in interval:
        print(rr["fname"])
    print("___________________________________________________")
    classif.set_roadrace()
    road_races = classif.mongo.simplequery("trainingtype.roadrace", True)
    for rr in road_races:
        print(rr["fname"])
    print("___________________________________________________")

    XX
